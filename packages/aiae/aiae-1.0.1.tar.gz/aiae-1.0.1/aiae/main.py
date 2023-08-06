import os
from aitkhelp import EntryBar, Browse, OkButton, Popup
from tkinter import *
from netz.parser import Parse
import matplotlib.pyplot as plt
from scipy import stats, integrate
import seaborn as sns
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
from pandas import to_numeric
import numpy as np

sns.set_theme()
sns.set()


def main():
    root = Tk()
    br = Browse(root)
    ions = EntryBar(root, picks=['Ion'])
    br.pack()
    ok = OkButton(root, function=lambda: c(br, ions, root))
    root.mainloop()


def c(files, ions, root):
    files = files.get()
    ion = list(ions.get('Ion'))
    grads = []
    try:
        for file in files:
            grads.append(read_csv(file, skiprows=34, sep=';', engine='python'))
    except:
        Popup(parent=root, text=f"Unable to load {file.name}")
    try:
        x = Netzsch(grads, ion)
        x.parse()
        x.alpha()
    except:
        Popup(parent=root, text=f"Some error I didn't account for happened. Check your data set for anything strange")
    out_path = os.path.split(file.name)[0]
    out_name = f'Calculated Parameters for {ion}.csv'
    if not x.critical:
        out_data = x.oak
        out_data.mean(axis=1).to_csv(os.path.join(out_path, out_name))
        x.plot()
    else:
        Popup(parent=root, text=x.error)


class Netzsch:
    REPLACE_STRINGS = ["##", "s:1|"]
    ACS = "Alpha Cumulative Sum"
    TIME = "Time/min"
    TEMP = "Temp./°C"

    GAS_CONSTANT = 8.3144598
    EPS = 1
    N = 1000
    K = 273.15
    KK = 1000

    def __init__(self, dataframes, ions):
        self.dataframes = dataframes
        self.ions = ions
        self.error = ''
        self.critical = False
        self.parsed_frames = []
        self.ion_column = ''
        self.oak = None
        self.X = None
        self.Y = None

    @staticmethod
    def qmid(ions: list):
        return [f"QMID(m:{ion})/A" for ion in ions]

    @staticmethod
    def current(ions: list):
        return [f"IonCurrent(m:{ion})/A" for ion in ions]

    def parse(self):
        for df in self.dataframes:
            df = df.rename(columns=lambda x: re.sub('##', '', x))
            df = df.rename(columns=lambda x: re.sub(r's:1\|', '', x))
            keys = ["Time/min", "Temp./°C"]
            if self.qmid(ions=self.ions)[0] in df.columns:
                self.ion_column = self.qmid(ions=self.ions)[0]
                keys.append(self.ion_column)
            elif self.current(ions=self.ions)[0] in df.columns:
                self.ion_column = self.current(ions=self.ions)[0]
                keys.append(self.ion_column)
            else:
                self.error = f"Your ion {self.ions} was not found anywhere in the dataset. Are you sure you entered the correct ion?"
                self.critical = True
            try:
                df = df[keys]
            except KeyError:
                self.error = f'Unable to find {keys}'
                self.critical = True
            self.parsed_frames.append(df)

    def alpha(self):
        frameDict = {}
        betadict = {}
        for frame in self.parsed_frames:
            workFrame = DataFrame()
            beta, temp_zero, dt, temp_start, temp_end = self.lineparams(frame)
            try:
                frame = frame.applymap(lambda x: x.strip()).replace('', '0').applymap(lambda x: float(x))
            except AttributeError:
                try:
                    frame = frame.applymap(lambda x: to_numeric(x, errors='coerce')).dropna()
                except AttributeError:
                    self.error = f"Unable to convert this frame to numeric data"
                    self.critical = True

            frame["T"] = frame.get(self.TIME).mul(beta).add(self.K + temp_start)
            workFrame["PreAlpha"] = frame.get(self.ion_column)
            workFrame["PreAlpha"].index = frame.get("T")
            workFrame["T"] = frame.get("T")
            workFrame = workFrame.set_index("T")
            integral = workFrame.apply(lambda g: integrate.simps(g, x=g.index))
            pre_alpha = workFrame.rolling(2).apply(lambda g: integrate.simps(g, x=g.index))
            workFrame["Alpha"] = pre_alpha.div(integral).cumsum().fillna(0)
            finalFrame = workFrame.drop(columns="PreAlpha").reset_index().set_index("Alpha")
            frameDict[f'{beta:.0f}'] = finalFrame
            betadict[f'{beta:.0f}'] = beta
        self.oak = self.Oakwood(frameDict, betadict, 0.6, 0.3)

    def Oakwood(self, frame, beta, alpha_max, alpha_min):
        area = np.arange(alpha_min, alpha_max, 0.01)
        X = []
        Y = []
        for alpha in area:
            x = [alpha]
            y = [alpha]
            for b in beta.keys():
                temp = self.nonlinearinterpol(alpha, frame[b])
                x.append((1 / temp) * 1000)
                y.append(np.log(beta[b] / np.power(float(temp), 2)))
            X.append(x)
            Y.append(y)
        DATASETS = {}
        for i in range(0, len(X)):
            slope, intercept, r_value, p_value, std_err = stats.linregress(X[i][1:], Y[i][1:])
            E = -(slope * self.GAS_CONSTANT)
            A = intercept
            DATASETS[X[i][0]] = [E, A, r_value, p_value, std_err]
        r = DataFrame.from_dict(DATASETS)
        r.index = ["Activation Energy", "Pre Exponential", "R", "P", "std_err"]
        self.X = X
        self.Y = Y
        self.beta = beta
        return r

    def nonlinearinterpol(self, alpha, frame):
        x0 = frame.loc[frame[frame.index < alpha].idxmax()].index[0]
        y0 = frame.loc[frame[frame.index < alpha].idxmax()]["T"].values[0]
        x1 = frame.loc[frame[frame.index > alpha].idxmin()].index[0]
        y1 = frame.loc[frame[frame.index > alpha].idxmin()]["T"].values[0]
        a = (alpha - x0)
        b = (x1 - x0)
        _c = (y1 - y0)
        return (a / b) * _c + y0

    def lineparams(self, frame):
        time = frame.get(self.TIME).astype(float)
        temp = frame.get(self.TEMP).astype(float)
        if len(time) == len(temp):
            X = sum(time)
            Y = sum(temp)
            XX = sum(map(lambda x: x * x, time))
            XY = sum(map(lambda time_temp: time_temp[0] * time_temp[1], zip(time, temp)))
            beta = (XY * len(time) - X * Y) / (len(time) * XX - X * X)
            temp_zero = (Y - beta * X) / (len(time))
            dt = time.diff().mean()
            temp_start = temp[0]
            temp_end = temp[temp.last_valid_index()]
            return beta, temp_zero, dt, temp_start, temp_end
        else:
            return 0


    def plot(self):
        Q = DataFrame([x[1:] for x in self.X], index=[x[0] for x in self.X])
        W = DataFrame([y[1:] for y in self.Y], index=[y[0] for y in self.Y])
        fig = plt.figure(num=None)
        _, ax = plt.subplots()
        ax.set_ylabel('ln(B / T^2)')
        for i, index in enumerate(Q.index[:-2]):
            if i % 10 == 0:
                temp = concat([Q.loc[index], W.loc[index]], axis=1)
                temp.columns = ['1 / Temp * 1000', f'{round(index, 2)}']
                temp.sort_values(by='1 / Temp * 1000', inplace=True)
                temp.plot(ax=ax, x='1 / Temp * 1000', y=f'{round(index, 2)}')
        plt.legend(frameon=False)
        plt.legend(framealpha=0.0)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def getAl(alpha, frame):
        b = frame.loc[frame[frame.index < alpha].idxmax()]["T"]
        c = frame.loc[frame[frame.index > alpha].idxmin()]["T"]
        alpha_temp = concat([b, c]).mean()
        return alpha_temp


if __name__ == "__main__":
    main()
