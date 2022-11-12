import argparse
import backtrader as bt
import strategies.stochrsi as stochrsi
import strategies.macdCrossover as macdCrossover
import strategies.bband as bband
import strategies.utils.util as util
import backtrader.analyzers as btanalyzers



def main(args):
    cb = bt.Cerebro()
    if args.strategy == 'stochrsi':
        cb.addstrategy(stochrsi.TestStrategy)
    elif args.strategy == 'macd':
        cb.addstrategy(macdCrossover.TestStrategy)
    elif args.strategy == 'bband':
        cb.addstrategy(bband.BBandStrategy)
    else:
        print('Invalid strategy')
        return
    data = bt.feeds.YahooFinanceCSVData(dataname=args.data)
    cb.adddata(data)
    cb.broker.setcash(args.cash)
    cb.addsizer(util.Sizer)
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
    print('Final Portfolio Value: %.2f' % cb.broker.getvalue())





if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Backtest')
    parser.add_argument('--strategy', type=str, default='stochrsi', help='Strategy to use')
    parser.add_argument('--data', type=str, default='data/TATAMOTORS.NS.csv', help='Data to use')
    parser.add_argument('--cash', type=float, default=100000.0, help='Starting cash')
    parser.add_argument('--commission', type=float, default=0.001, help='Commission')
    parser.add_argument('--sizer', type=str, default='util.Sizer', help='Sizer')
    parser.add_argument('--plot', type=bool, default=False, help='Plot')
    args = parser.parse_args()
    main(args)