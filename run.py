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
        # self.a_start = 1


def main(argv):

    parser=argparse.ArgumentParser()

    parser.add_argument('--url', help='Start URL', default='https://scholar.google.com/citations?view_op=search_authors&mauthors=machine+learning&hl=ko&oi=drw')
    parser.add_argument('--interval', help='Save Data Interval', type=int, default=1000)
    parser.add_argument('--max_count', help='Max Count of Crawling Scholars', type=int, default=10000)
    parser.add_argument('--start', help='Start Point of Crawling Scholars', type=int, default=0)
    parser.add_argument('--file_path', help='Crawling File Path', default='1_10000.csv')
    parser.add_argument('--max_author_count', help='Max Count of Author when Crawling scholars', type=int, default=100)
    parser.add_argument('--author_link', help='if you want to crawling scholar', action='store_true', default=False)
    parser.add_argument('--scholar_link', help='if you want to crawling scholar', action='store_true', default=False)
    parser.add_argument('--author', help='if you want to crawling author', action='store_true', default=False)
    parser.add_argument('--scholar', help='if you want to crawling scholar', action='store_true', default=False)

    args=parser.parse_args()

    # assert args.author or args.scholar, 'You must use either option --author or --scholar.'

    gf = GlobalInfo(args.interval)

    al, sl, a, s = make_save_directory()

    if args.author_link:
        crawling_author_links(gf, args.url, args.max_count)
    if args.scholar_link:
      crawling_scholar_links(gf, args.url, args.max_count)
    if args.author:
        crawling_authors(gf, al, args.max_count)
    if args.scholar:
        crawling_scholars_by_author(gf, f'{al}/{args.file_path}', args.start, args.max_author_count)
        # crawling(gf, args.url, args.max_count)
        # crawling_scholars(gf, sl, args.max_count)
    
if __name__ == "__main__":
    main(sys.argv)