# Plot Cleaning Function Explanations

## HTML Decoding
We found many instances of html entities throughout our plot summaries and we didn't want it to harm the RAG process. So we applied ``html.unescape()`` which is used to convert named and numeric character references such as ``&gt;``, ``&#62;``, ``&#x3e;``, ``&mdash;`` into their corresponding unicode characters. 

Example:
- "Chester staggers to a piano and plays Narcissa's ballad ``&mdash;`` the saddest music in the world ``&mdash;`` as he burns in the fire." 
Results:
- "Chester staggers to a piano and plays Narcissa's ballad — the saddest music in the world — as he burns in the fire."

**References**:
- https://www.geeksforgeeks.org/python/re-sub-python-regex/
- https://docs.python.org/3/library/html.html
- https://www.geeksforgeeks.org/machine-learning/python-efficient-text-data-cleaning/

---

## Regex Patterns

**References:** 
- https://docs.python.org/3/library/re.html#module-contents
- https://flipperfile.com/developer-guides/regex/regex-to-remove-html/

### Remove Wiki Templates
``re.sub(r"\{\{[^{}]*\}\}", " ", text)`` 

This regex was used to replace anything within two curly brackets `{{...}}`
- `r""` --> raw string so `\` is treated literally  
- `\{\{` --> match opening brackets `{{`. 
    - Note: need escape (`\`) since `{` is used. 
- `[^{}]` --> match any character **except** ``{}``
- `*` --> repeat previous pattern **0 or more times**  
- `\}\}` --> match closing bracketets `}}`  

The reason we used this was because we found instanances of content within curly brackets. Such as ``{{plot}}``, ``{{tone}}``, ``{{Expand section}}``, ``{{long plot}}`` and more.

---
 
### Remove refs tags: `<ref>`, `<ref>...<ref>`
`re.sub(r"<ref[^>]*>.*?</ref>", " ", text, flags=re.IGNORECASE | re.DOTALL)`

This regex was used to remove any `<ref>...</ref>` tags. `re.IGNORECASE` performs case-incensitive matching so `<ref>` or `<REF>` will be matched. `re.DOTALL` makes `.` match any character at all including new lines. Without this parameter, `.` will match anything except new lines. This is used to ensure `.*?` doesn't stop at a new line.
- `<ref` --> opening tag `<ref`
- `[^>]` --> match any character **except** `>`
- `*` --> repeat previous pattern **0 or more times**
- `>` --> end of opening tag  
- `.*?` --> match any character up until the next `<ref>` tag 
- `</ref>` --> closing tag  

`re.sub(r"<ref[^>]*/\s*>", " ", text, flags=re.IGNORECASE)`

Similarly this regex removes any single ref tag `<ref....>`
- `<ref` --> matches a opening tag
- `[^>]` --> matches anything except `>`
- `*` --> repeat this 0+ times
-  `/` --> literal slash
    - `<ref name="source"/>` (to match)
- `/s` --> any white space character
- `>` --> closing tag

Overall these regex were used to removed `<ref>...<ref>` and `<ref....>`. 

---

### HTML tags
`r"<[^>]+>"`

This regex is used for removing HTML tags such as `<span>`, `<div>`, and similar markup.

- `r""` --> raw string so `\` is treated literally  
- `<` --> opening tag
- `[^>]` --> match anything except `>`
- `+` 1+ occurences of the pattern:
    - `<...`
- `>` closing tag

--- 

### Remove actors mentioned following a character
`re.sub(r"\(\[\[\s*[A-Z][a-z]+(?:[\s_]+[A-Z][a-z]+){0,3}(?:_+)?\s*,?")`

This is a more specialized pattern designed to match the start of a actor's name written in broken wiki links after a character's name. Example: `([[Patrick Gallagher,` or `([[Matt_Damon,`

- `\(` --> matches a literal `(`
- `\[\[` --> matches the wiki opening brackets `[[`
- `\s*` --> matches 0+ whitespace characters
- `[A-Z]` --> matches one uppercase letters
- `[a-z]+` --> matches 1+ lowercase letters, completing a capitalized name part
- `(?:[\s_]+[A-Z][a-z]+){0,3}` --> matches 0-3 additional capitalized name parts, separated by spaces or underscores
- `(?:_+)?` --> optionally matches one or more underscores left at the end
- `\s*` --> matches optional whitespace
- `,?` --> optionally matches a comma

In our plot summaries we found that some actor's name were inserted right after the previously mentioned character. 

For example:
- `"Boris ([[Andy Jones, a familiar blue collar worker, is issued his orders for a patient transfer"`

Turns into:
- `"Boris, a familiar blue collar worker, is issued his orders for a patient transfer"`.

---

### Convert Wiki Links
`re.sub(r"\[\[([^|\]]+)\|([^\]]+)\]\]", r"\2")`

This regex finds wiki links that contain a pipe, such as `[[Tom_and_Jerry|Tom and Jerry]]`, and replaces the full link with only the displayed text after the pipe (in the example it'll return `Tom and Jerry`).

- `\[\[` --> matches the opening wiki brackets `[[`
- `(` --> starts capture group 1
- `[^|\]]+` --> matches 1+ characters that aren't `|` or `]`
- `)` --> ends capture group 1
- `\|` --> matches a literal pipe character `|`
- `(` --> starts capture group 2
- `[^\]]+` --> matches 1+ characters that aren't `]`
- `)` --> ends capture group 2
- `\]\]` --> matches the closing wiki brackets `]]`
- `r"\2"` --> replaces the full match with capture group 2, which is the text after the pipe

For example:
- `The film follows [[Tom_and_Jerry|Tom and Jerry]] as they cause chaos in a hotel while [[Kayla Forester|Kayla]] tries to keep her job.`

Turns into:
- `The film follows Tom and Jerry as they cause chaos in a hotel while Kayla tries to keep her job.`

`re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)`

Matches simple wiki links such as `[[Titanic]]`, where there is no pipe and the linked page name is also the visible text. It allows us to remove the wrapper `[[ ]]`, while keeping what's inside. 

- `\[\[` --> matches the opening wiki brackets `[[`
- `(` --> starts capture group 1
- `[^\]]+` --> matches 1+ characters that aren't `]`
- `)` --> ends capture group 1
- `\]\]` --> matches the closing wiki brackets `]]`
- `r"\1"` --> replaces the full match with capture group 1, which is the text inside the brackets

For example:
- `The plot follows [[Titanic]] as it depicts the romance between [[Jack Dawson]] and [[Rose DeWitt Bukater]] during the ship's doomed voyage.`

Turns into:
- `The plot follows Titanic as it depicts the romance between Jack Dawson and Rose DeWitt Bukater during the ship's doomed voyage.`

---

### Normalize White Spaces
`re.sub(r"\s+", " ", text)`

Removes extra white spaces in text.

- `\s` --> matches any whitespace character
- `+` --> repeats the previous pattern 1+ times

---

### Remove URLs
`re.sub(r"http\S+|www\.\S+"`

Removes URLs that start with `http` or `www`.

- `r""` --> raw string 
- `htpp` --> match `http`
- `\S+` --> 1+ non white-space character
- `|` --> or 
- `www\.` --> match `www.`
    - `\.` escapes `.` allowing for `www.`
- `\S+` --> 1+ non white-space character
