# Python Markdown On-Page SEO

An SEO tool that analyzes the content of markdown before publishing.

Requires Python 3+, Markdown 3.3.4, and BeautifulSoup4.

## Installation

`git clone git@github.com:apowell656/python-markdown-on-page-seo.git`

## Command-line Usage

If you want to check a markdown document without front matter.

```
cd python-markdown-on-page-seo
./onpageseo.py filename.md example.com no_fm "focus keyword"
```

By default, it will use the first H1 tag for the title of the document and the first paragraph's first 160 characters as the meta description. To provide another string to be used add the following options.

```
cd python-markdown-on-page-seo
./onpageseo.py filename.md example.com no_fm "focus keyword" -t "My preferred title" -d "My preferred meta description"
```

Do the following to check a document containing front matter. *You must add the field that contains the focus keywords. The script will use the first phrase found as the focus keyword.*

```
cd python-markdown-on-page-seo
./onpageseo.py filename.md example.com fm tags
```

Just like a markdown document without front matter, it will use the first paragraph for the meta description. You can change this behavior by adding the name of the field containing the meta description.

```
cd python-markdown-on-page-seo
./onpageseo.py filename.md example.com fm tags -dl summary
```

## Sample Output

```
./onpageseo.py README.md example.com no_fm markdown

Title
===============================================================================
Python Markdown On-Page SEO
Length of Title: 27
The focus keyword is in the title.

SEO Behind This Section: Google typically displays the first 50 - 60 characters and 
staying under 60 means most of your titles will fully display in SERPs.

Meta Description
===============================================================================
An SEO tool that analyzes the content of markdown before publishing.
The focus keyword was found in the description or the first paragraph.
It will be displayed in the meta description if the SSG uses the first paragraph for this tag.

SEO Behind This Section: The focus keyword should appear in the meta description of the page and be 50 - 160 characters.
Reference(s): https://rankmath.com/kb/score-100-in-tests/#focus-keyword-in-the-meta-description-primary-focus-keyword-only 
and https://moz.com/learn/seo/meta-description

Word Count
===============================================================================
A 459 word count is a good start for your content.

SEO Behind This Section: SEO best practices are not clear on what Google and other search engines consider a good length for content.
I have settled on a minimum of 300 - 500 words.
Reference(s): https://rankmath.com/kb/score-100-in-tests/#overall-content-length

Keyword Count & Density
===============================================================================
The focus keyword 'markdown' has been used 14 times with a keyword density of 3.05%.

SEO Behind This Section: It is recommended that your focus keyword should appear between 1 - 1.5%.
Reference(s): https://rankmath.com/kb/score-100-in-tests/#Keyword%20Density%20.

Images
===============================================================================
There are no identifiable images.

Links
===============================================================================
SEO best practices recommend 3 links and there are none in your content.

SEO Behind This Section: Providing both internal and external links is a good way for your site to build credibility.
Reference(s): https://rankmath.com/kb/score-100-in-tests/#linking-to-internal-resources and 
https://rankmath.com/kb/score-100-in-tests/#linking-to-external-sources

Internal Links
*******************************************************************************
There are no internal links.

External Links
*******************************************************************************
There are no external links.

Content Structure
===============================================================================

SEO Behind This Section: Using additional sub-headings helps readers and search engines understand the structure of your content.
Reference(s): https://rankmath.com/kb/score-100-in-tests/#focus-keyword-in-subheading-primary-and-secondary-focus-keywords

H2 Heading(s) without Keyword
*******************************************************************************
Installation
Command-line Usage
Sample Output
```

## Why Make This?  

Since moving away from WordPress I cannot use [RankMath](https://rankmath.com/) to review my content's on-page SEO before publishing. I use the [Python SEO Analyzer](https://github.com/sethblack/python-seo-analyzer) to make sure my sites are not missing any basics, but needed something to review my content, especially before publishing.
