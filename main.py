import argparse
import random
import re
import time
import warnings
import urllib3

warnings.simplefilter("ignore", urllib3.exceptions.InsecureRequestWarning)


def generate_domain_list(domain_text):
    # 顶级域列表
    tld_list = ['ac', 'academy', 'agency', 'app' 'arpa', 'art', 'asia', 'at', 'auto', 'autos', 'baby', 'band', 'bd', 'beauty', 'beer', 'best', 'bio', 'biz', 'black', 'blog', 'blue', 'bond', 'buzz', 'ca', 'cab', 'cafe', 'car', 'care', 'cars', 'casa', 'cash', 'cc', 'center', 'chat', 'church', 'city', 'click', 'cloud', 'club', 'cn', 'co', 'college', 'com', 'com.cn', 'company', 'cool', 'cyou', 'date', 'de', 'design', 'dev', 'directory', 'dog', 'download', 'edu', 'email', 'fail', 'faith', 'fan', 'fans', 'fashion', 'finance', 'fit', 'foundation', 'fun', 'fund', 'games', 'global', 'gold', 'golf', 'gov', 'green', 'group', 'guide', 'guru', 'hair', 'help', 'host', 'house', 'icu', 'immo', 'in', 'info', 'ink', 'io', 'kim', 'la', 'lan', 'law', 'life', 'link', 'live', 'loan', 'local', 'love', 'ltd', 'luxe', 'makeup', 'market', 'marketing', 'mba', 'me', 'media', 'men', 'mil', 'mobi', 'moe', 'money', 'monster', 'motorcycles', 'mx', 'name', 'net', 'net.cn', 'network', 'news', 'nl', 'one', 'online', 'ooo', 'org', 'org.cn', 'organic', 'party', 'pet', 'photos', 'pink', 'plus', 'poker', 'press', 'pro', 'promo', 'protection', 'pub', 'pw', 'quest', 'red', 'ren', 'rent', 'review', 'rip', 'run', 'school', 'science', 'security', 'services', 'sh', 'shop', 'shopping', 'show', 'site', 'ski', 'skin', 'social', 'solutions', 'space', 'storage', 'store', 'stream', 'studio', 'support', 'systems', 'tax', 'team', 'tech', 'technology', 'theatre', 'tickets', 'tips', 'today', 'tools', 'top', 'trade', 'tv', 'uno', 'us', 'video', 'vin', 'vip', 'vote', 'voto', 'wang', 'website', 'wiki', 'win', 'work', 'works', 'world', 'ws', 'wtf', 'xin', 'xyz', 'yoga', 'zone']

    if domain_text is not None:
        domain_list = [f"{domain_text}.{tld}" for tld in tld_list]
    else:
        alphabet = "abcdefghijklmnopqrstuvwxyz1234567890"
        domain_text = "".join(random.sample(alphabet, 12))
        domain_list = [f"{domain_text}.{tld}" for tld in tld_list]
    # print(domain_list)
    return domain_list


def check_https_response(domain, ip):
    try:
        pool = urllib3.HTTPSConnectionPool(
            host=ip,
            assert_hostname=domain,
            server_hostname=domain,
            retries=urllib3.util.Retry(
                total=0
            ),
            cert_reqs='CERT_NONE'
        )
        rs = pool.urlopen("GET", "/", headers={"Host": domain}, assert_same_host=False)
        print(f"OK [{rs.status}] - {domain}")
        return 'ok'
    except urllib3.exceptions.MaxRetryError as e:
        if isinstance(e.reason, urllib3.exceptions.ProtocolError):
            if "ConnectionResetError" in str(e.reason):
                print(f"RST - {domain}")
                return 'rst'
    except Exception as e:
        pass
    print(f"OK [-1] - {domain}")
    return 'ok'


def check_domain_whitelist(domain_text=None, domain_text_len=12, ip="104.16.123.96", timeout=3):
    domain_ok = []
    domain_rst = []
    if domain_text is None:
        alphabet = "abcdefghijklmnopqrstuvwxyz1234567890"
        domain_text = "".join(random.sample(alphabet, domain_text_len))
    print(f'生成域名列表 [{domain_text}.*] ')
    domain_list = generate_domain_list(domain_text)

    for domain in domain_list:
        rs = check_https_response(domain, ip)
        if rs == 'rst':
            domain_rst.append(domain.replace(f"{domain_text}.", ""))
        else:
            domain_ok.append(domain.replace(f"{domain_text}.", ""))
    print(f"正常 [{len(domain_ok)}]： {domain_ok}")
    print(f"重置 [{len(domain_rst)}]： {domain_rst}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="DomainWhitelistCheck")
    parser.add_argument("-i", required=True, help="IP")
    parser.add_argument("-d", required=False, default=None, help="Domain")
    args = parser.parse_args()
    if not re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", args.i):
        print('输入 IP 格式有误')
        time.sleep(3)

    check_domain_whitelist(domain_text=args.d, ip=args.i, domain_text_len=12)
    input('\n\n按任意键退出')


