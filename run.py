import argparse, sys
import os

from save_result import *
from crawling_func import *

class GlobalInfo:
    def __init__(self, interval = 1000):
        # 저장 단위
        self.interval = interval

        # 논문 데이터 카운트
        self.start = 1

        # 저자 데이터 카운트
        self.a_start = 1


def main(argv):

    parser=argparse.ArgumentParser()

    parser.add_argument('--url', help='Start URL', default='https://scholar.google.com/citations?view_op=search_authors&mauthors=machine+learning&hl=ko&oi=drw')
    parser.add_argument('--interval', help='Save Data Interval', type=int, default=1000)
    parser.add_argument('--max_scholar', help='Max Count of Crawling Scholars', type=int, default=10000)
    parser.add_argument('--max_author', help='Max Count of Crawling Authors', type=int, default = 1000)
    parser.add_argument('--author', help='if you want to crawling author', action='store_true', default=False)
    parser.add_argument('--scholar', help='if you want to crawling scholar', action='store_true', default=False)

    args=parser.parse_args()

    assert args.author or args.scholar, 'You must use either option --author or --scholar.'

    gf = GlobalInfo(args.interval)

    make_save_directory()

    crawling(gf, args.url, args.max_scholar, args.max_author, args.author, args.scholar)
    
if __name__ == "__main__":
    main(sys.argv)