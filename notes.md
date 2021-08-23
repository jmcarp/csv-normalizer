Questions:
- Is it safe to assume rfc-compliant csvs (values with commas in
    quotes, quote characters escaped)?
  - Yes
- Is it safe to assume timestamps are month/day/year hour:minute:second am/pm?
  - Yes
- Will timestamps ever include timezones?
  - No
- Will zip codes ever contain >5 digits? Non-digit characters?
  - No
- Will durations ever be negative?
  - No
- How should invalid data be handled? For example, invalid timestamps,
    non-numeric zip codes, invalid durations
  - As you see fit.
- Re "please convert them to the total number of seconds": should this
    be a float or an int?
  - Float
- Will input documents always include a header line? If not, will input columns always appear in the same order?
  - Yes/yes
- Should script exit with nonzero status code on bad input?
