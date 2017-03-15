# Major Webscraping for OIE

**Language**: `Python v3.5`

**Library Used**:
- Native Library
  - `urllib`: Requesting web response
  - `os`: Creating a file
  - `csv`: Creating `.csv` file
- Third Party Library
  - `BeautifulSoup`: Reading and Parsing html.

**Webscraping Logic**

1. Read html from `baseURL` and `degree_programURL`.
2. Find target tags (`div` -> `ul` -> `li` )
3. Store it into dictionary (`Link` and `Major Name`)
4. Grab all present links.
5. From that link go to specific tags(`div` -> `section` -> `p`)
6. Grab all the present link and parse it if it has `#`.
7. After that write it.
