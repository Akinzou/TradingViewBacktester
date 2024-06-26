import pandas as pd
from datetime import datetime

class Backtester:
    def setValues(self, invert, sl, tp, spreadpips, position_path, prices_path, printfunc):
        self.invert = bool(invert)
        self.sl = float(sl)
        if self.sl > 0:
            self.sl = self.sl * -1
        self.tp = float(tp)
        self.spread_pips = float(spreadpips)
        self.pips = 1 / self.spread_pips
        self.position_path = position_path
        self.prices_path = prices_path
        self.printfunc = printfunc

    def findmedian(self, prices):
        if len(prices) != 0:
            self.printfunc(self.pips)
            self.printfunc(prices)
            prices_sorted = sorted(prices)
            n = len(prices_sorted)
            srodek = n // 2

            # Jeśli liczba elementów jest parzysta
            if n % 2 == 0:
                return str(round((prices_sorted[srodek - 1] + prices_sorted[srodek]) / 2, 2)) + " pips"
            # Jeśli liczba elementów jest nieparzysta
            else:
                return str(round(prices_sorted[srodek], 2)) + " pips"
        else:
            return "Only tp/sl"

    def readPNLlist(self):
        return self.PNLlist

    def readPositionList(self):
        return self.positions

    def readSummary(self):
        message = (f'Overall:\n'
                  f'PNL: {round(self.PNL, 2)} pips\n'
                  f'Num of SL: {self.num_of_sl}\n'
                  f'Num of TP: {self.num_of_tp}\n'
                  f'Winrate: {round((self.wins / (self.wins + self.loss)) * 100, 2)}%\n'
                  f'TPrate: {self.calculateTPrate()}\n'
                  f'Wins: {self.wins}, Loss: {self.loss}\n'
                  f'Median loss: {self.findmedian(self.losslist)}\n'
                  f'Median win: {self.findmedian(self.winslist)}\n'
                  f'\n\n'
                   f'Configs:\n'
                   f'SL: {self.sl}\n'
                   f'TP: {self.tp}\n'
                   f'Invert: {self.invert}\n'
                   f'Spread pips: {self.spread_pips}\n'
                   f'Positions path: {self.position_path}\n'
                   f'Prices path: {self.prices_path}\n'
                  )
        return message

    def  calculateTPrate(self):
        if self.num_of_tp + self.num_of_sl > 0:
            return  str(round((self.num_of_tp / (self.num_of_tp + self.num_of_sl)) * 100, 2)) + "%"
        else:
            return "No TP/SL"

    def runbacktester(self):
        self.PNL = 0
        self.entry_price = 0
        self.floatinPLN = 0
        self.loss = 0
        self.wins = 0
        self.num_of_sl = 0
        self.num_of_tp = 0
        self.losslist = []
        self.winslist = []
        self.positions = []
        self.PNLlist = []

        # Wczytywanie danych
        positions_df = pd.read_csv(self.position_path)
        prices_df = pd.read_csv(self.prices_path)

        # Praca na positions_df
        positions_types = positions_df['Type'].tolist()
        positions_dates = positions_df['Date/Time'].tolist()  # Dodanie listy dla daty/czasu

        # Usuwanie dwóch pierwszych elementów z list
        positions_types = positions_types[2:]
        positions_dates = positions_dates[2:]

        # Odwracanie list
        positions_types.reverse()
        positions_dates.reverse()

        # Praca na prices_df
        prices_df = prices_df.iloc[:, 0].str.split('\t', expand=True)
        prices_columns = ['DATE', 'TIME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'TICKVOL', 'VOL', 'SPREAD']
        prices_df.columns = prices_columns

        # Konwersja DATE i TIME do datetime
        prices_df['DATE'] = pd.to_datetime(prices_df['DATE'], format='%Y.%m.%d')
        prices_df['TIME'] = pd.to_datetime(prices_df['TIME'], format='%H:%M:%S').dt.time

        # Połączenie DATE i TIME w jedną kolumnę DATETIME
        prices_df['DATETIME'] = pd.to_datetime(prices_df['DATE'].astype(str) + ' ' + prices_df['TIME'].astype(str))

        # Formatowanie DATETIME do formatu bez sekund
        prices_df['DATETIME'] = prices_df['DATETIME'].dt.strftime('%Y-%m-%d %H:%M')

        # Tworzenie listy prices_dates z połączonej kolumny DATETIME bez sekund
        prices_dates = prices_df['DATETIME'].tolist()

        # Usunięcie zbędnych kolumn
        prices_df.drop(columns=['DATE', 'TIME'], inplace=True)

        prices_close = prices_df['CLOSE'].tolist()
        prices_high = prices_df['HIGH'].tolist()
        prices_low = prices_df['LOW'].tolist()

        if self.invert:
            self.printfunc("Inverting:")
            print(positions_types)
            for i in range(len(positions_types)):
                original_value = positions_types[i]

                if original_value == 'Entry Long':
                    positions_types[i] = 'Entry Short'
                elif original_value == 'Exit Long':
                    positions_types[i] = 'Exit Short'
                elif original_value == 'Entry Short':
                    positions_types[i] = 'Entry Long'
                elif original_value == 'Exit Short':
                    positions_types[i] = 'Exit Long'
            print(positions_types)
            self.printfunc("Done")
            self.printfunc("---------")

        positions_date = datetime.strptime(positions_dates[0], '%Y-%m-%d %H:%M')
        prices_date = datetime.strptime(prices_dates[0], '%Y-%m-%d %H:%M')

        for i in range(len(positions_types) - 1):
            positions_date = datetime.strptime(positions_dates[i], '%Y-%m-%d %H:%M')
            positions_date_close = datetime.strptime(positions_dates[i + 1], '%Y-%m-%d %H:%M')
            prices_date = datetime.strptime(prices_dates[i], '%Y-%m-%d %H:%M')
            # search entry price
            for x in range(len(prices_dates)):
                found_entry = False
                if positions_types[i] == 'Entry Short' or positions_types[i] == 'Entry Long':
                    prices_date = datetime.strptime(prices_dates[x], '%Y-%m-%d %H:%M')
                    if prices_date == positions_date:
                        if positions_types[i] == 'Entry Short':
                            self.entry_price = float(prices_low[x])
                        elif positions_types[i] == 'Entry Long':
                            self.entry_price = float(prices_high[x])
                        found_entry = True
                        self.printfunc(f"{positions_date}, {self.entry_price}")

                # search exit price
                if found_entry:
                    if positions_types[i] == 'Entry Short':
                        self.printfunc("Looking for exit price for short...")
                        for y in range(x, len(prices_dates)):
                            close_price_date = datetime.strptime(prices_dates[y], '%Y-%m-%d %H:%M')
                            if positions_date <= close_price_date < positions_date_close:
                                self.floatinPLN = (self.entry_price - float(prices_high[y])) * self.pips
                                if self.floatinPLN <= self.sl:
                                    self.PNL += self.sl
                                    self.positions.append(self.sl)
                                    self.loss += 1
                                    self.num_of_sl += 1
                                    self.PNLlist.append(self.PNL)
                                    break

                                self.floatinPLN = (self.entry_price - float(prices_low[y])) * self.pips
                                if self.floatinPLN >= self.tp:
                                    self.PNL += self.tp
                                    self.positions.append(self.tp)
                                    self.wins += 1
                                    self.num_of_tp += 1
                                    self.PNLlist.append(self.PNL)
                                    break

                            elif close_price_date >= positions_date_close:
                                self.floatinPLN = (self.entry_price - float(prices_high[y])) * self.pips
                                if self.floatinPLN <= self.sl:
                                    self.PNL += self.sl
                                    self.positions.append(self.sl)
                                    self.loss += 1
                                    self.num_of_sl += 1
                                    self.PNLlist.append(self.PNL)
                                    break

                                self.floatinPLN = (self.entry_price - float(prices_low[y])) * self.pips
                                if self.floatinPLN >= self.tp:
                                    self.positions.append(self.tp)
                                    self.PNL += self.tp
                                    self.wins += 1
                                    self.num_of_tp += 1
                                    self.PNLlist.append(self.PNL)
                                    break

                                self.floatinPLN = (self.entry_price - float(prices_close[y])) * self.pips
                                if self.floatinPLN < 0:
                                    self.PNL += self.floatinPLN
                                    self.positions.append(self.floatinPLN)
                                    self.losslist.append(self.floatinPLN)
                                    self.loss += 1
                                    self.PNLlist.append(self.PNL)
                                    break

                                if self.floatinPLN >= 0:
                                    self.PNL += self.floatinPLN
                                    self.positions.append(self.floatinPLN)
                                    self.wins += 1
                                    self.winslist.append(self.floatinPLN)
                                    self.PNLlist.append(self.PNL)
                                    break

                    if positions_types[i] == 'Entry Long':
                        self.printfunc("Looking for exit price for long...")
                        for y in range(x, len(prices_dates)):
                            close_price_date = datetime.strptime(prices_dates[y], '%Y-%m-%d %H:%M')
                            if positions_date <= close_price_date < positions_date_close:
                                self.floatinPLN = (float(prices_low[y]) - self.entry_price) * self.pips
                                if self.floatinPLN <= self.sl:
                                    self.positions.append(self.sl)
                                    self.PNL += self.sl
                                    self.loss += 1
                                    self.num_of_sl += 1
                                    self.PNLlist.append(self.PNL)
                                    break

                                self.floatinPLN = (float(prices_high[y]) - self.entry_price) * self.pips
                                if self.floatinPLN >= self.tp:
                                    self.positions.append(self.tp)
                                    self.PNL += self.tp
                                    self.wins += 1
                                    self.num_of_tp += 1
                                    self.PNLlist.append(self.PNL)
                                    break

                            elif close_price_date >= positions_date_close:
                                self.floatinPLN = (float(prices_low[y]) - self.entry_price) * self.pips
                                if self.floatinPLN <= self.sl:
                                    self.positions.append(self.sl)
                                    self.PNL += self.sl
                                    self.loss += 1
                                    self.num_of_sl += 1
                                    self.PNLlist.append(self.PNL)
                                    break

                                self.floatinPLN = (float(prices_high[y]) - self.entry_price) * self.pips
                                if self.floatinPLN >= self.tp:
                                    self.positions.append(self.tp)
                                    self.PNL += self.tp
                                    self.wins += 1
                                    self.num_of_tp += 1
                                    self.PNLlist.append(self.PNL)
                                    break

                                self.floatinPLN = (float(prices_close[y]) - self.entry_price) * self.pips
                                if self.floatinPLN < 0:
                                    self.positions.append(self.floatinPLN)
                                    self.PNL += self.floatinPLN
                                    self.losslist.append(self.floatinPLN)
                                    self.loss += 1
                                    self.PNLlist.append(self.PNL)
                                    break

                                if self.floatinPLN >= 0:
                                    self.PNL += self.floatinPLN
                                    self.winslist.append(self.floatinPLN)
                                    self.positions.append(self.floatinPLN)
                                    self.wins += 1
                                    self.PNLlist.append(self.PNL)
                                    break

        self.printfunc("---------------------------------------------------------------")

