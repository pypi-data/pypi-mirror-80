import json
import sys
from collections import deque

from prettyparse import Usage
from shibboleth_get import shibboleth_get

usage = Usage('''
    Mediaspace m3u8 extractor using Selenium
    
    :username str
        Illinois netid to use
    :password str
        Corresponding password for netid
    :-j --json
        Output as json lines
    :-t --title
        Output title of video
    :-q --quiet
        Hide status output
    ...
''')
usage.add_argument('mediaspace_urls', help='Mediaspace URLs to extract m3u8 from', nargs='*')
usage.add_argument('-m', '--metadata', type=json.loads, default={}, help='Extra json metadata to attach to each element')


def main():
    args = usage.parse()
    if not args.mediaspace_urls:
        return
    driver = shibboleth_get(args.username, args.password, args.mediaspace_urls[0], debug=not args.quiet)
    driver.implicitly_wait(10)
    metadatas = args.metadata
    if isinstance(metadatas, dict):
        metadatas = [metadatas] * len(args.mediaspace_urls)
    urls = deque(list(zip(args.mediaspace_urls, metadatas)))
    is_first = True
    while urls:
        url, metadata = urls.popleft()
        if not args.quiet:
            print('Processing {}...'.format(dict(url=url, **metadata)), file=sys.stderr)
        if is_first:
            is_first = False
        else:
            driver.get(url)
        if 'channel' in url.lower():
            links = driver.find_elements_by_css_selector('#gallery .isotope-item .thumb_name:nth-child(2) .item_link')
            if not args.quiet:
                print('Found {} links.'.format(len(links)), file=sys.stderr)
            for link in reversed(links):
                urls.appendleft((link.get_attribute('href'), metadata))
            continue
        try:
            iframe = driver.find_element_by_css_selector('iframe#kplayer_ifp')
        except Exception:
            print('Saving screenshot to problem.png...', file=sys.stderr)
            driver.get_screenshot_as_file("problem.png")
            raise
        title = driver.find_element_by_css_selector('.entryTitle').text
        driver.switch_to.frame(iframe)
        vid = driver.find_element_by_tag_name('video')
        src = vid.get_attribute('src')
        data = [
            ('src', src)
        ]
        if args.title:
            data += [('title', title)]
        for key, val in metadata.items():
            data += [(key, val)]
        if args.json:
            print(json.dumps(dict(data)))
        else:
            for _, value in data:
                print(value)
    driver.quit()


if __name__ == '__main__':
    main()
