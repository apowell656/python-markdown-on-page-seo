#!/usr/bin/env python3

import argparse
import markdown
import re
from bs4 import BeautifulSoup


class bcolors:
    OK = '\033[92m'  # GREEN
    WARNING = '\033[93m'  # YELLOW
    FAIL = '\033[91m'  # RED
    RESET = '\033[0m'  # RESET COLOR


def separator_length(a_string, target_length):
    number_of_repeats = target_length // len(a_string) + 1
    a_string_repeated = '\n' + a_string * number_of_repeats
    a_string_repeated_to_target = a_string_repeated[:target_length]
    return a_string_repeated_to_target


def section_heading(heading):
    section = '\n' + heading
    section_divider = separator_length('=', 80)
    final_heading = section + section_divider
    return final_heading


def sub_section_heading(heading):
    section = '\n' + heading
    section_divider = separator_length('*', 80)
    final_heading = section + section_divider
    return final_heading


def main():
    parser = argparse.ArgumentParser(
        description='Reviews the  SEO of a Markdown document')

    # Required/Positional arguments
    parser.add_argument('file', help='The file to be analyzed.')

    parser.add_argument(
        'domain', help='The domain used to check if links are internal or external.')

    # Sub commands for documents with and without front matter
    subparsers = parser.add_subparsers(
        help='Select based on if the document has front matter or not.', dest='front_matter')
    parser_fm = subparsers.add_parser(
        'fm', help='Use this option when a document has front matter. When using this subcommand it will look for a field named "Title" and you must add the name of the field that has the focus keyword to be analyzed and optionally the field used for your meta description. Usage: python-markdown-seo.py FILE DOMAIN FM KW_LOOKUP OPTIONAL: -dl|--desc_lookup DESC_LOOKUP Example: python-markdown-seo.py file.md example.com fm tags --dl summary')
    parser_no_fm = subparsers.add_parser(
        'no_fm', help='Use this option when a document does not have front matter. When using this subcommand you must add the keyword to be analyzed. Usage: python-markdown-seo.py FILE DOMAIN NO_FM KEYWORD OPTIONAL: -t|--title "Your content title" -d|--desc "Your description" Example: python-markdown-seo-py file.md example.com no_fm "focus keyword".')

    # Arguments for documents with front matter
    parser_fm.add_argument(
        'kw_lookup', help='Name of front matter field that holds keywords i.e. "tags".')
    parser_fm.add_argument(
        '-dl', '--desc_lookup', help='Name of front matter field that holds the meta description i.e. "summary".')

    # Arguments for documents without front matter
    parser_no_fm.add_argument(
        'focus_keyword', help='Manually add the focus keyword when there is no front matter.')
    parser_no_fm.add_argument(
        '-t', '--title', help='Manually enter the title used for your content.')
    parser_no_fm.add_argument(
        '-d', '--desc', help='Manually enter the meta description. Default: Use the first 160 characters of the first paragraph to determine the meta description if one not entered.')

    # [Placeholder] Optional arguments

    args = parser.parse_args()

    file = args.file
    domain = args.domain

    md = markdown.Markdown(extensions=['meta'])
    with open(file, 'r', encoding='utf-8') as input_file:
        text = input_file.read()
    html = md.convert(text)
    front_matter = md.Meta
    post = BeautifulSoup(html, 'html.parser')

    if args.front_matter == 'fm':
        keywords = md.Meta[args.kw_lookup.lower()][0]
        primary = keywords.split(',')
        focus_keyword = primary[0]

    else:
        focus_keyword = args.focus_keyword

    # If there is front matter the 'title' will be used instead.
    if args.front_matter == 'fm':
        title = front_matter['title'][0]
    elif args.title:
        title = args.title
        print(args.title)
    else:
        if post.find_all('h1'):
            get_title = post.find_all('h1')[0]
            title = get_title.get_text()

    # Get the length of the title
    title_length = len(title)
    # For longer titles try to put the keyword in the first 50% of the title string
    placement_max = title_length/2
    focus_keyword_title_placement = f'{bcolors.FAIL}The focus keyword does not appear in the title or it is not at the beginning of the title.{bcolors.RESET}'

    # The focus keyword should be in the title of the article
    title_focus_keyword_search = re.search(
        focus_keyword, title, flags=re.IGNORECASE)
    if title_focus_keyword_search:
        focus_keyword_title_placement = f'{bcolors.OK}The focus keyword is in the title.{bcolors.RESET}'
    elif title_focus_keyword_search and title_focus_keyword_search.span()[1] <= placement_max:
        focus_keyword_title_placement = f'{bcolors.OK}The focus keyword is in the title and placed at the beginning.{bcolors.RESET}'
    else:
        focus_keyword_title_placement = f'{bcolors.FAIL}The keyword does not appear in the title.{bcolors.RESET}'

    print(section_heading('Title'))
    print(title)
    if title_length <= 60:
        print(bcolors.OK + 'Length of Title: ' +
              str(title_length) + bcolors.RESET)
    else:
        print(bcolors.FAIL + 'Length of Title: ' +
              str(title_length) + bcolors.RESET)
    print(focus_keyword_title_placement)
    print('\nSEO Behind This Section: Google typically displays the first 50 - 60 characters and \nstaying under 60 means most of your titles will fully display in SERPs.')

    # SEO best practices recommend that the focus keyword be in the first paragraph of your content
    get_first_paragraph = post.find_all('p')[0]
    first_paragraph = get_first_paragraph.get_text()

    # Some of SSGs (Static Site Generators) can use the contents of your first paragraph
    # as the meta description of your HTML document. The default is to check the first
    # paragraph for the focus keyword.
    if args.front_matter == 'fm':
        meta_description = first_paragraph[0: 160:]
    if args.front_matter == 'fm' and  args.desc_lookup:
        meta_description = front_matter[args.desc_lookup.lower()][0]        
    elif args.front_matter == 'no_fm' and args.desc is not None:
        meta_description = args.desc
    else:
        meta_description = first_paragraph[0: 160:]

    meta_description_length = len(meta_description)
    focus_keyword_meta_description_placement = 'The focus keyword does not appear in the meta description.'
    meta_description_keyword_search = re.search(
        focus_keyword, meta_description, flags=re.IGNORECASE)
    if meta_description_keyword_search:
        focus_keyword_meta_description_placement = f'{bcolors.OK}The focus keyword was found in the description or the first paragraph.\nIt will be displayed in the meta description if the SSG uses the first paragraph for this tag.{bcolors.RESET}'
    else:
        focus_keyword_meta_description_placement = 'The focus keyword was not found in the first 160 characters of the description or the first paragraph. (Based on your settings)'

    print(section_heading('Meta Description'))
    print(meta_description)
    print(focus_keyword_meta_description_placement)
    print('\nSEO Behind This Section: The focus keyword should appear in the meta description of the page and be 50 - 160 characters.\nReference(s): https://rankmath.com/kb/score-100-in-tests/#focus-keyword-in-the-meta-description-primary-focus-keyword-only \nand https://moz.com/learn/seo/meta-description')

    # SEO best practices are not clear on what 'Google' considers a good length
    # for content. I have settled on on a minimum of 300 - 500 words.
    word_count = 0
    content = post.find_all('p')
    for word in content:
        x = word.get_text()
        word_count += len(x.split())

    print(section_heading('Word Count'))
    if word_count < 300:
        word_count_summary = 'A ' + \
            str(word_count) + \
            ' word count is below the recommendation of a 300 - 500 word minimum.'
        print(bcolors.FAIL + word_count_summary + bcolors.RESET)
    elif word_count >= 300 and word_count <= 500:
        word_count_summary = 'A ' + \
            str(word_count) + ' word count is a good start for your content.'
        print(bcolors.OK + word_count_summary + bcolors.RESET)
    else:
        word_count_summary = 'A ' + \
            str(word_count) + \
            ' word count will help your content gain traction in search engines. Good job!'
        print(bcolors.OK + word_count_summary + bcolors.RESET)
    print('\nSEO Behind This Section: SEO best practices are not clear on what Google and other search engines consider a good length for content.\nI have settled on a minimum of 300 - 500 words.\nReference(s): https://rankmath.com/kb/score-100-in-tests/#overall-content-length')

    # SEO best practices recommend the number of times your focus keyword appears
    # should between 1 - 1.5% https://rankmath.com/kb/score-100-in-tests/. This script will tell you
    # your result, how many words you should have, how many you have, and the difference.
    focus_keyword_count_target = int(round(word_count * .01, 0))
    focus_keyword_content_count = len(
        post(text=re.compile(focus_keyword, re.IGNORECASE)))
    keyword_density = round(focus_keyword_content_count / word_count, 4)*100
    keyword_difference = focus_keyword_content_count - focus_keyword_count_target
    keyword_summary = 'The focus keyword \'' + focus_keyword + '\' has been used ' + \
        str(focus_keyword_content_count) + \
        ' times with a keyword density of '+str(keyword_density) + '%.'

    if keyword_density < .75:
        keyword_summary_format = bcolors.FAIL + keyword_summary + bcolors.RESET
    elif keyword_density >= .75 and keyword_density < 1:
        keyword_summary_format = bcolors.WARNING + keyword_summary + bcolors.RESET
    else:
        keyword_summary_format = keyword_summary

    print(section_heading('Keyword Count & Density'))
    print(keyword_summary_format)

    if keyword_difference < 0:
        keyword_error = 'The target use is ' + \
            str(focus_keyword_count_target) + ' and the keyword appears ' + \
            str(focus_keyword_content_count) + ' times in the content.'
        keyword_guidance = 'Add the keyword ' + \
            str(keyword_difference * -1) + \
            ' more times to be between 1 - 1.5% KWD.'
        print(bcolors.FAIL + keyword_error + bcolors.RESET)
        print(bcolors.FAIL + keyword_guidance + bcolors.RESET)
    print('\nSEO Behind This Section: It is recommended that your focus keyword should appear between 1 - 1.5%.\nReference(s): https://rankmath.com/kb/score-100-in-tests/#Keyword%20Density%20.')

    # SEO best practices recommend at least on image be in your content. The image
    # should have the focus keyword in the alt tag and be used in the name of the file.
    # I have found good Google Search Console results with images. Checking the name
    # of the file is done visually.
    get_images = post.find_all('img')
    image_count = len(get_images)
    images_with_focus_keyword_in_alt = []
    images_without_focus_keyword_in_alt = []

    for image in get_images:
        alt_text = image.get('alt')
        keyword_in_alt = re.search(
            focus_keyword, alt_text, flags=re.IGNORECASE)
        if keyword_in_alt:
            images_with_focus_keyword_in_alt.append(image)
        else:
            images_without_focus_keyword_in_alt.append(image)

    print(section_heading('Images'))
    if image_count >= 1:
        print(bcolors.OK + str(image_count) +
              ' image(s) were found in your content. Good job!' + bcolors.RESET)
        print('\nSEO Behind This Section: Adding media to your content helps improve your SEO standing. Currently, this script looks for at least one image.\nBe sure to add the focus keyword in the alt tag of your images and try to include it in the name of the file.\nReference(s): https://rankmath.com/kb/score-100-in-tests/#use-of-media-in-your-posts and https://moz.com/learn/seo/alt-text')
        if len(images_with_focus_keyword_in_alt) > 0:
            print(sub_section_heading('Images with keyword in alt tag'))
            for img in images_with_focus_keyword_in_alt:
                print(bcolors.OK + str(img) + bcolors.RESET)
        if len(images_without_focus_keyword_in_alt) > 0:
            print(sub_section_heading('Images without the keyword in alt tag'))
            for img in images_without_focus_keyword_in_alt:
                print(bcolors.WARNING + str(img) + bcolors.RESET)
    else:
        print(bcolors.FAIL + 'There are no identifiable images.' + bcolors.RESET)

    # SEO best practices recommend 3 links. This one is easy, but linking to internal
    # content will help improve your sites standing with search engines.
    links = post.find_all('a')
    link_count = 0
    internal_link_count = 0
    internal_links = []
    external_link_count = 0
    external_links = []
    for link in links:
        link_count += 1
        link_url = link.get('href')
        domain_in_link = re.search(domain, link_url, flags=re.IGNORECASE)
        if domain_in_link:
            internal_links.append(link)
        else:
            external_links.append(link)
            external_link_count += 1

    print(section_heading('Links'))
    if link_count > 0:
        link_summary = str(link_count) + ' links were found in your content.'
        print(bcolors.OK + link_summary + bcolors.RESET)
    else:
        print(bcolors.WARNING +
              'SEO best practices recommend 3 links and there are none in your content.' + bcolors.RESET)
    print('\nSEO Behind This Section: Providing both internal and external links is a good way for your site to build credibility.\nReference(s): https://rankmath.com/kb/score-100-in-tests/#linking-to-internal-resources and \nhttps://rankmath.com/kb/score-100-in-tests/#linking-to-external-sources')
    print(sub_section_heading('Internal Links'))
    if internal_link_count < 1:
        print(bcolors.WARNING + 'There are no internal links.' + bcolors.RESET)
    else:
        print(bcolors.OK + str(internal_link_count) +
              ' internal links exist in your content.\n' + bcolors.RESET)
    if internal_link_count > 0:
        for link in internal_links:
            print(link)

    print(sub_section_heading('External Links'))
    if external_link_count < 1:
        print(bcolors.WARNING + 'There are no external links.' + bcolors.RESET)
    elif external_link_count >= 1 and external_link_count <= 2:
        print(bcolors.WARNING + str(external_link_count) +
              ' external links exist.\n' + bcolors.RESET)
    else:
        print(bcolors.OK + str(external_link_count) +
              ' external links exist.\n' + bcolors.RESET)
    if external_link_count > 0:
        for link in external_links:
            print(link)

    # Additional headings help to improve the organization of your content. If you
    # are using h2 - h6 headers place your focus keyword or related keywords for
    # additional search engine juice.
    other_headings_count = 0
    h2_with_focus_keyword = []
    h2_without_focus_keyword = []
    h3_count = []
    h3_with_focus_keyword = []
    h3_without_focus_keyword = []
    h4_count = []
    h4_with_focus_keyword = []
    h4_without_focus_keyword = []
    h5_count = []
    h5_with_focus_keyword = []
    h5_without_focus_keyword = []
    h6_count = []
    h6_with_focus_keyword = []
    h6_without_focus_keyword = []

    h2_list = post.find_all('h2')
    h2_count = len(h2_list)
    h3_list = post.find_all('h3')
    h3_count = len(h3_list)
    h4_list = post.find_all('h4')
    h4_count = len(h4_list)
    h5_list = post.find_all('h5')
    h5_count = len(h5_list)
    h6_list = post.find_all('h6')
    h6_count = len(h6_list)

    for h in h2_list:
        text = h.get_text()
        find_keyword = re.search(focus_keyword, text, flags=re.IGNORECASE)
        if find_keyword:
            h2_with_focus_keyword.append(text)
            other_headings_count += 1
        else:
            h2_without_focus_keyword.append(text)
            other_headings_count += 1

    for h in h3_list:
        text = h.get_text()
        find_keyword = re.search(focus_keyword, text, flags=re.IGNORECASE)
        if find_keyword:
            h3_with_focus_keyword.append(text)
            other_headings_count += 1
        else:
            h3_without_focus_keyword.append(text)
            other_headings_count += 1

    for h in h4_list:
        text = h.get_text()
        find_keyword = re.search(focus_keyword, text, flags=re.IGNORECASE)
        if find_keyword:
            h4_with_focus_keyword.append(text)
            other_headings_count += 1
        else:
            h4_without_focus_keyword.append(text)
            other_headings_count += 1

    for h in h5_list:
        text = h.get_text()
        find_keyword = re.search(focus_keyword, text, flags=re.IGNORECASE)
        if find_keyword:
            h5_with_focus_keyword.append(text)
            other_headings_count += 1
        else:
            h5_without_focus_keyword.append(text)
            other_headings_count += 1

    for h in h6_list:
        text = h.get_text()
        find_keyword = re.search(focus_keyword, text, flags=re.IGNORECASE)
        if find_keyword:
            h6_with_focus_keyword.append(text)
            other_headings_count += 1
        else:
            h6_without_focus_keyword.append(text)
            other_headings_count += 1

    if other_headings_count > 0:
        print(section_heading('Content Structure'))
        print('\nSEO Behind This Section: Using additional sub-headings helps readers and search engines understand the structure of your content.\nReference(s): https://rankmath.com/kb/score-100-in-tests/#focus-keyword-in-subheading-primary-and-secondary-focus-keywords')
    if h2_count > 0:
        if len(h2_with_focus_keyword) > 0:
            print(sub_section_heading('H2 Heading(s) with Keyword'))
            for heading in h2_with_focus_keyword:
                print(heading)
        if len(h2_without_focus_keyword) > 0:
            print(sub_section_heading('H2 Heading(s) without Keyword'))
            for heading in h2_without_focus_keyword:
                print(heading)

    if h3_count > 0:
        if len(h3_with_focus_keyword) > 0:
            print(sub_section_heading('H3 Heading(s) with Keyword'))
            for heading in h3_with_focus_keyword:
                print(heading)
        if len(h3_without_focus_keyword) > 0:
            print(sub_section_heading('H3 Heading(s) without Keyword'))
            for heading in h3_without_focus_keyword:
                print(heading)

    if h4_count > 0:
        if len(h4_with_focus_keyword) > 0:
            print(sub_section_heading('H4 Heading(s) with Keyword'))
            for heading in h4_with_focus_keyword:
                print(heading)
        if len(h4_without_focus_keyword) > 0:
            print(sub_section_heading('H4 Heading(s) without Keyword'))
            for heading in h4_without_focus_keyword:
                print(heading)

    if h5_count > 0:
        if len(h5_with_focus_keyword) > 0:
            print(sub_section_heading('H5 Heading(s) with Keyword'))
            for heading in h5_with_focus_keyword:
                print(heading)
        if len(h5_without_focus_keyword) > 0:
            print(sub_section_heading('H5 Heading(s) without Keyword'))
            for heading in h5_without_focus_keyword:
                print(heading)

    if h6_count > 0:
        if len(h6_with_focus_keyword) > 0:
            print(sub_section_heading('H6 Heading(s) with Keyword'))
            for heading in h6_with_focus_keyword:
                print(heading)
        if len(h6_without_focus_keyword) > 0:
            print(sub_section_heading('H6 Heading(s) without Keyword'))
            for heading in h6_without_focus_keyword:
                print(heading)


if __name__ == '__main__':
    main()
