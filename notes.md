Questions:
- Is it safe to assume rfc-compliant csvs?
- Is it safe to assume timestamps are month/day/year hour:minute:second am/pm?
- Will timestamps ever include timezones?
- Will zip codes ever contain >5 digits? Non-digit characters?
- Will durations every be negative?
- How should invalid data be handled? For example, invalid timestamps,
    non-numeric zip codes, invalid durations
- Re "please convert them to the total number of seconds": should this
    be a float or an int?
- Will input documents always include a header line?
