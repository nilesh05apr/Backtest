import argparse
import backtrader as bt
import strategies.stochrsi as stochrsi
import strategies.macdCrossover as macdCrossover
import strategies.mInd.macdRsi as macdrsi
import strategies.bband as bband
import strategies.adx as adx
import strategies.kdj as kdj
import strategies.utils.util as util
import backtrader.analyzers as btanalyzers
import yfinance as yf


def main(args):
    cb = bt.Cerebro()
    if args.strategy == 'stochrsi':
        cb.addstrategy(stochrsi.TestStrategy)
    elif args.strategy == 'macd':
        cb.addstrategy(macdCrossover.TestStrategy)
    elif args.strategy == 'bband':
        cb.addstrategy(bband.BBandStrategy)
    elif args.strategy == 'adx':
        cb.addstrategy(adx.TestStrategy)
    elif args.strategy == 'kdj':
        cb.addstrategy(kdj.KDJStrategy)
    elif args.strategy == 'macdrsi':
        cb.addstrategy(macdrsi.MACDRSI)
    else:
        print('Invalid strategy')
        return
    if args.data == 'yahoo':
        data = bt.feeds.YahooFinanceCSVData(dataname=args.data_dir)
    elif args.data == 'yfinance':
        data = yf.download(args.ticker, start=args.start, end=args.end)
        data = bt.feeds.PandasData(dataname=data)
    else:
        print('Invalid data')
        return
    cb.adddata(data)
    cb.broker.setcash(args.cash)
    cb.addsizer(util.Sizer, risk=args.risk)
    start = cb.broker.getvalue()
    print('Starting Portfolio Value: %.2f' % cb.broker.getvalue())
    cb.addanalyzer(btanalyzers.SharpeRatio, _name='sharpe')
    cb.addanalyzer(btanalyzers.DrawDown, _name='drawdown')
    cb.addanalyzer(btanalyzers.Returns, _name='returns')
    thestrats = cb.run()
    thestrat = thestrats[0]

    print('\n\n','-'*30,'ANALYSIS','-'*30)
    print('\n')
    #print('Sharpe Ratio:', thestrat.analyzers.sharpe.get_analysis())
    sharperatio = thestrat.analyzers.sharpe.get_analysis()
    sharperatio = list(sharperatio.items())[0]
    print('Sharpe Ratio:', sharperatio[1])

    
    print('\n',' '*10,'-'*10,'Returns','-'*10)
    returns = thestrat.analyzers.returns.get_analysis()
    returns = list(returns.items())
    for k,v in returns:
        print(k,':',v)

    
    print('\n',' '*10,'-'*10,'DrawDowns','-'*10)
    drawdown = thestrat.analyzers.drawdown.get_analysis()
    drawdown = list(drawdown.items())
    for k,v in drawdown:
        if k == 'max':
            max = list(v.items())
            for k2,v2 in max:
                print(k2,':',v2)
        else:
            print(k,':',v)
    print('\n')
    print('-'*30,'END ANALYSIS','-'*30)
    end = cb.broker.getvalue()
    print('Final Portfolio Value: %.2f' % cb.broker.getvalue())
    print('Profit: %.2f' % (end - start))
    print('Profit Percentage: %.2f%%' % ((end - start) / start * 100))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Backtest')
    parser.add_argument('--strategy', type=str, default='stochrsi', help='Strategy to use')
    parser.add_argument('--data', type=str, default='yahoo', help='Data to use')
    parser.add_argument('--data_dir', type=str, default='data/TATAMOTORS.NS.csv', help='Data directory')
    parser.add_argument('--ticker', type=str, default='TATAMOTORS.NS', help='Ticker to use')
    parser.add_argument('--start', type=str, default='2019-01-01', help='Start date')
    parser.add_argument('--end', type=str, default='2020-01-01', help='End date')
    parser.add_argument('--cash', type=float, default=100000.0, help='Starting cash')
    parser.add_argument('--commission', type=float, default=0.001, help='Commission')
    parser.add_argument('--risk', type=float, default=0.01, help='Risk')
    args = parser.parse_args()
    main(args)