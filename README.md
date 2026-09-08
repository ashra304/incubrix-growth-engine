\# IncuBrix Growth Engine



A creator discovery and lead qualification engine designed to discover YouTube creators, collect publicly available evidence, evaluate qualification criteria, and produce structured lead data.



\## Overview



The IncuBrix Growth Engine follows a structured pipeline:



YouTube Discovery

→ Activity Verification

→ Evidence Collection

→ Lead Construction

→ Qualification

→ Priority

→ Personalization

→ Completeness

→ Duplicate Check

→ Deduplication

→ CSV Export



The system is designed so that discovery does not automatically mean qualification. A creator must satisfy the defined qualification and evidence requirements before becoming a final lead.



\## Core Features



\### YouTube Discovery

Discovers creator channels using the YouTube Data API and stores stable creator identifiers and profile information.



\### Activity Verification

Collects recent publishing activity, including:



\- Content published in the last 30 days

\- Long-form content in the last 60 days

\- Most recent content date

\- Recent content URL



\### Evidence Collection



The engine collects and evaluates public evidence for:



\- Country

\- Primary language

\- Commercial activity

\- IncuBrix-relevant creator/business needs

\- Public business contact information



\### Qualification



Creators are evaluated against defined qualification rules including:



\- Approved creator segment

\- Approved country

\- English-language content

\- Official profile

\- Stable creator ID

\- Recent activity

\- Commercial activity

\- IncuBrix-relevant need

\- Public business contact

\- Required fields

\- Uniqueness

\- Fresh evidence



\### Priority



Qualified creators receive a priority classification based on the available commercial, need, contact, and activity signals.



\### Personalization



The engine generates a short personalization hook based on publicly observed creator signals.



\### Completeness



Every Lead is checked for required fields before becoming part of the final qualified dataset.



\### Duplicate Detection



Creators are checked using stable identity signals:



1\. Stable creator ID

2\. Profile URL

3\. Website URL

4\. Lead ID



\### CSV Export



Final qualified leads are exported to:



`data/final\_leads.csv`



\## Project Structure



```text

incubrix-growth-engine/

│

├── config/

│   ├── .env.example

│   └── settings.py

│

├── data/

│   ├── leads.csv

│   └── final\_leads.csv

│

├── docs/

│   └── README.md

│

├── src/

│   ├── completeness.py

│   ├── creator\_discovery.py

│   ├── deduplication.py

│   ├── duplicate\_check.py

│   ├── evidence.py

│   ├── exporter.py

│   ├── freshness.py

│   ├── lead\_builder.py

│   ├── lead\_loader.py

│   ├── lead\_schema.py

│   ├── personalization.py

│   ├── pipeline.py

│   ├── priority.py

│   ├── qualification.py

│   ├── qualification\_engine.py

│   ├── source\_schema.py

│   │

│   └── sources/

│       └── youtube.py

│

└── tests/

&#x20;   ├── test\_completeness.py

&#x20;   ├── test\_contact.py

&#x20;   ├── test\_deduplication.py

&#x20;   ├── test\_discovery.py

&#x20;   ├── test\_duplicate\_check.py

&#x20;   ├── test\_end\_to\_end.py

&#x20;   ├── test\_evidence.py

&#x20;   ├── test\_exporter.py

&#x20;   ├── test\_freshness.py

&#x20;   ├── test\_lead\_builder.py

&#x20;   ├── test\_loader.py

&#x20;   ├── test\_personalization.py

&#x20;   ├── test\_priority.py

&#x20;   ├── test\_qualification.py

&#x20;   ├── test\_qualification\_engine.py

&#x20;   ├── test\_source\_schema.py

&#x20;   └── test\_youtube\_source.py

