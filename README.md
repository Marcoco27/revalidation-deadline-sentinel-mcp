# Revalidation Deadline Sentinel

When must this US healthcare provider revalidate its Medicare enrollment, and has CMS set the date yet?

Every Medicare provider or supplier must revalidate its enrollment information (in PECOS or on the CMS-855 forms) on the due date CMS sets, at least every five years (42 CFR 424.515). CMS publishes the due dates in a monthly list, sends a notice about three to four months ahead, and does not grant extensions: a late revalidation can lead to a hold on Medicare payments or to deactivation of billing privileges.

For 1 to 50 NPI numbers, this MCP server and HTTP API return each Medicare enrollment (enrollment ID for organizations only, state, Part A, DME or Non-DME Part B, provider type, specialty) with:

- the due date exactly as published in the latest CMS Revalidation Due Date List (data.cms.gov), never computed or guessed;
- the days left, counted in the enrollment state's time zone;
- a status: `upcoming`, `date_passed`, or `not_set` when CMS has not set the date yet (which does not mean nothing is due);
- the version of the list read (for example `2026-11-01`).

When both date fields of the list are filled, `due_date` is the earlier one and the other is returned apart. No weekend or holiday shift is applied. No names are read or returned.

- MCP (streamable HTTP): `https://revalidation.amacunia.fr/mcp`, tools `revalidation_lookup` (paid, 0.01 USDC per call via x402 on Base) and `revalidation_example` (free).
- HTTP: `GET https://revalidation.amacunia.fr/v1/revalidation?npi=1306897277` (x402, 0.01 USDC; free trial: 3 calls per day).
- Free sample: `https://revalidation.amacunia.fr/v1/exemple`.
- Machine-readable: `/llms.txt`, `/.well-known/x402`, `/terms`.
- Paying client example: [`examples/pay_mcp.py`](examples/pay_mcp.py).

No account, no API key.

## Data

CMS Revalidation Due Date List, data.cms.gov, monthly. U.S. Government work, public domain (source attribution: CMS). Only these fields are read: enrollment ID, NPI, enrollment state, enrollment type, provider type, specialty, revalidation due date and adjusted due date.

## Disclaimer

Information only, not legal advice; it does not replace a qualified attorney. Not affiliated with or endorsed by the Centers for Medicare & Medicaid Services (CMS), the U.S. Department of Health and Human Services or any U.S. government agency. Not a consumer report under the FCRA: do not use it to decide on employment, credit or insurance. CMS may request off-cycle revalidations that are not in the list; the CMS Medicare Revalidation List tool (https://data.cms.gov/tools/medicare-revalidation-list) and your CMS notice are the authoritative record. Terms of use: https://revalidation.amacunia.fr/terms. Contact: contact@amacunia.fr
