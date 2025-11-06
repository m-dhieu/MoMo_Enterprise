# MoMo SMS Processing Application

## Table of contents

* [Overview](#overview)
* [Features](#features)
* [Demo Video](#demo-video)
* [Repository Structure](#repository-structure)
* [Architecture](#architecture)
* [Database](#database)
* [API Server](#api-server)
* [DSA Comparison](#data-structures-&-algorithms-(dsa)-comparison)
* [Development Workflow](#development-workflow)
* [Environment](#environment)
* [Team](#team)
* [Setup Instructions](#setup-instructions)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)

## Overview

This repository contains an enterprise-level full-stack application for processing Mobile Money (MoMo) SMS data.  
The system ingests SMS data in XML format, performs data cleaning and categorization, persists the results in a relational database, provides a REST API for transaction data, and offers a frontend dashboard for analytics and visualization.

## Features

* XML parsing using `xml.etree.ElementTree`  
* Data cleaning and normalization (dates, amounts, phone numbers)  
* Transaction categorization (payments, withdrawals, transfers, etc.)  
* Relational database persistence (MySQL)  
* REST API server in plain Python with Basic Authentication  
* Data Structures & Algorithms performance comparison (linear search vs dictionary lookup)  
* JSON exports for dashboard analytics  
* Frontend visualization (charts)  
* Modular ETL pipeline (`parse` → `clean` → `categorize` → `load` → `export`)  
* Unit tests for core ETL stages

## Demo Video

[Demo Video](https://youtu.be/FLaZANm46pw) to walk-through how to visualize data in the dashboard UI.

## Repository Structure

```
MoMo_Enterprise/
├── README.md                    # Setup, run, overview 
├── CONTRIBUTING.md              # PRs, branching, and issues guide     
├── setup_project.sh             # Environment setup script
├── .gitignore                   # Files for Git to ignore    
├── .env                         # Environment configs, DB URLs/path to SQLite
├── requirements.txt             # Python dependencies
├── web/			 # web assets, Architecture diagram
├── data/
│   ├── raw/                     # Original XML (gitignored)
│   ├── processed/               # JSON exports
│   └── logs/                    # ETL logs, dead letter files
├── database/                    # DB files
├── examples/
│   └── json_schemas.json        # JSON schema
├── api/                         
│   ├── server.py                # REST API server
├── dsa/
│   ├── parse_xml.py             # XML parser
│   └── compare_dsa_search.py    # DSA comparison
├── docs/			 # ERD design rationale, API documentation, team report
├── screenshots			 # Test Screenshots 
└── tests/                       # Unit tests
```

## Architecture

The system follows a modular design:  
* Data ingestion from SMS XML loaded into ETL pipeline  
* Processing: parsing, cleaning, normalization, categorization  
* Persistence: relational database + caching layer  
* API: transaction data served securely via REST  
* DSA: search performance comparisons  
* Frontend: static dashboard consuming aggregated data  

View Architecture Diagram on [web](https://viewer.diagrams.net/?tags=%7B%7D&lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1&title=MoMo%20SMS%20Enterprise%20Architecture.drawio&dark=auto#R%3Cmxfile%3E%3Cdiagram%20id%3D%22C5RBs43oDa-KdzZeNtuy%22%20name%3D%22Page-1%22%3E7V1bd9q4Fv41rNU%2BhOX75ZFw6cxpk8kk6XTmKcuAAz4lmDGmac6vP5JtGVuSsWQk41DoWiUIWxZbn7b2XT19%2BPLzU%2BRtljfh3F%2F1NGX%2Bs6ePepqmKoqjg3fY9JY2mY7qpi2LKJhnl%2B0bHoL%2F%2BejerHUXzP1t6cI4DFdxsCk3zsL12p%2FFpTYvisLX8mXP4ar81I238ImGh5m3Ilu%2FBfN4mbY6mr1v%2F80PFkv0ZNXKft%2FUm31fROFunT1vBS%2B6mnvR9w89TZ8kr542zP%2F%2BmN724qFnZATYLr15%2BFpo0sc9fRiFYZz%2B9fJz6K8g1RE5v%2F3%2B9m315bv16T9%2Fbv%2F1vl5%2Ffrz96yrtbMJzS%2F7LI38dN%2B76%2Buv9art5%2B%2FO%2FprmI7paflO9fZ1eqkxHph7faZYTOfm38higPibfp6dfPwWo1DFdhBJrriahfLyJvHoAh89yzjaPwu89zByNxyuj0pujHZZP7w49i%2F2cBaRkRP%2Fnhix9Hb%2BCSfC0ZGYmylXTloiXyuselplpZ47IASs1FrV62GhZ5%2F%2FupA39ks8czk7ZSP5PL%2BAV0OlIB2ebedunDDhXw4XUZxP7DxpvB614BB2GfbXeip%2FPwHO5nGnzxnLyIGQXfWBMFvKgzV4PR%2Bjk65Qw4NvtS8gBF15Cw%2FnPcgBLHo9jQ3BKITY3EsKlSCKi7suhn0OhnrSB95sGPEh2tf3eQ616DHxtfZbQcgCtycqILwF%2BL7D3paLvx1tSe9pvE1SyFKuwvjrz1Fk3LNWzAHjgD3%2FjRwUfCdUF9ZOE5hfUVLaYflGRtKejtY%2FpO%2B%2BbjwUdPI7wFTEw6HqI5pQzRnFC%2B3HqZjMtkXCbjMhm%2FymRUUqbB%2FIkjpiIFCt4LlE7W0%2B0mvbvDTSl06JOVtn2phxNxfwXETrk6WmIE4SGytDUIbw6%2BB9Kxt575Uc08VUxpRXOJQ2BSefITDipDBcWpWi9SrwfqWEv1orHFrRcpijUeTHqEcgCE%2FdgL1pBiIw61KVdHuLSmlmV%2BVdFZlSa%2BXy1AQ1JKCpKuE%2FqRoRt9ZH4qkSs3ewknl1pPre3S28A%2FX34uoCmwv%2Fbj1zD6vtX6ASAKhNd2k9rnnoOfEPQHEK0krxTR6d%2BkjWZ%2FGWnxAd%2BZ15Zq6ZB5p%2BPQfgejeECmNLXwxXQxKQxkHa7Br7heeVN%2FdRdugziAgx%2FlvANOZDDzVl%2BwC6ZhHIcvhVVE3DHIvojDDTYsKtUWq3DqYxd%2Bw4YO237L2orLVWVfrvuVUI%2FQDJKWRarsGglH1EZDY9b3PVwq6wWAUA7%2FK1MpLwBkXyo%2BjcIrDIxVeCtA%2FbUX%2B9eQyW6JJZD%2FrOarAg2DYjjI943R7QN9OzlmKzhkrKQvHbgZZKZ1jccEpjJjI7dSliZPdfsmMX2IpRWnT9VlsS5NNuuCu%2B4I%2FvvlWNRsFe7m2IX%2F%2FPH8vPUhra6UvuLQGFgfUMSgcDGlb2sQWzJYV%2FatbpklfFo2gU7LpW6upixRxKTtrTXSP%2FziapusZyjYAlr9rJPl04bh6JZLum2XS0mcd9spzbtLciXkXSlxJXlek3qu5M8X%2FkP2MYziZbgI195qvG%2B9Lk%2FH%2FpovIVy%2FyST814%2Fjt4zze7s45JkidXQ93E9R0U%2BGHKFNFus23EUz%2F8CVGWliL1r4B3vMOoR0OoiByF95cfCj7M8VPqUag0bRwpT6P4P475TLqm72%2BZ%2BEuRqKmX0e%2Fcz6Tz68FT7c%2BVEAyJHrfGBOo7e%2Fk9uVhDUnDWl%2FuuWihn2Hyae34ie8y1NgThxEslvvwiBhzRl7ASJxX9Hd%2FcsqcRvH7eumsn9hgnG6IrIui5507Cm6pfddS7ENonNbcRzUuVXuPF1GROeiZOBq31kLpisF3wcN1n3w6xaaeZSR%2FyMAvIjf3kOx%2B5K2K5p5mfaAKiNyu%2F2fYL5UlXW%2BvvnTqymM5Umsc2LMuTfhNFj5V95m08zgx2bZU%2BsFJd74FnYOalnDYb0t8BjOyqMZYqK3Sohg1MgJW5YMxhCBRNeLavWrSs2MULwKKAh38SpYg2lFYWwKqWc%2Bm%2FAfTc%2B0kldBzxwFEegmff4ayhHU6a7SfPsrb5P%2BWIreOk3%2ByQWLXgaLS4LFoGBFk2cvfn9gsQzbcmwaWHTV0E1DHFheEk56gM%2FIAwpQzDFpiOQqCrJBlaBiyoKK0w09YC%2B5myW5vUZm76RKiFS9ep3Q6JROqDLohLUMojCpdBZDMIryHGbmwkPeluvxREunFb6yacVWu%2Fe%2FXeSn%2Fz%2BtQm%2F%2BNEXu0jalBtUmdwIWd4C4KTX4NZ7G5roThgEAibu3j3eokIJPMK4HPwLo2TYLsWBU5cRNJE1FY1EnqrVAWo9nqYnkgeKSnJkVDEYzT62XaAzO9ndiG0bGSKVv6U5vb4yErqG8oZE1Mutvb4103dw8yWONFC%2BqGIyiii1aUqkwTSIZBG2gOtYFq%2FVRw1Qy1cI6kmxp1Ggb74FlkYk9DZBfXjo5hnslY7rmcsO3k6I1KwxLClXG%2Bo6EpkHX8XmBaR7upgKWgyjy3gqXbeAFUsJEbOb8HM65FZBTppfDNTSHsvlRI%2FMMWeK1WSNes8SHkgLZYBcvAVWB7pRoV0Jc4C3LU8Pkld5hWPCfFMtujlau8E0qSJCTWzhIbIsXJGnDvRfDSLMvwQtQsteLCwyEwOCtPNunQwVpeBuPPo17Bc9P%2Bj%2FpG6rJnmBO3bi7Hz%2BMbx8HjzQ4%2Fl6vA9JSAOgsrmE2Sdr2RwPt%2BXji3Fb%2BUGxtwR6JVZCJc4St65kMjDtgMHsJ5vNEPaKt2LLcV1xSnCGWOrofyaKUTHphBnDS4K3btB1bgLpKTXAnV91teIBdKuUJokjiVIm9QF01NW%2FPB7C4A%2Fg8XYWz72kTjJLMtT1US8Ih%2BGCi3qI4S3hx4oO5zrNKMDzVK9us04u8E7XSdja5Sh%2FaY8si2pGyN7okTMM0DwnWAI3lUBPXwMQ%2BVhGd6EmFEaBtao80sRLDqJgiBcVknAlQ4yZOs2QcXkixcwxHKafg27QUfCoLkZaOY9N88eS%2BdT0Yfh7fjup39MEd2GyVh%2FH9X78Pxw%2BVu12DfSfb3c5r12mAIae8nm3TIDBkaJK2IeqPYPC0iVngA01RoPM4FdnH1%2BPrzlQhqaixobqUHBpVpbnN5EU86zSr9ukiBZldcA83gH8on4Dm%2BArtRR3TGMeZW4U11n4ycV1dP860yA9I1bQxROomBZE0fiEv7YLTnNwZL8vep4LCuf%2Fp7UO%2FK6zRueOkV3Ka5JEhB4NBjgGJOH8JCtiR7TCxdL2PeTo0u6Hc66oY7lXccMptna4YtEnI18rBkdmWe9wNjlG6HvyRjlmo1I4ETmGmc4GFrHAC6hbJ0gyaGG3gHjhxYjSDlsNDLkT%2BI6hVHexLpY0uzauuKgwMn4c4iNjHQ%2BnKUPt28VXOVcunoVQuoXyLQ4GZtGBYBkKKEbXtwUBVrdw6box0rixBg3kiukJZuxs5ZLwUrt3kdZdxk0elBToSv4nG%2Fd6UlqE3W%2FI6uI6OhlOtbHhKExJAhxP8e%2F9eX58obfhw78%2BD7UcBSTzvlwQj%2BEzCKKYMwKp%2Fi4MZkBwViAlfBJVa0Gvz4q6seq3rGsNikZhGITPs%2BwX61rD6WvFVNtXrtPq8itu3LPXQ9iJNBELFDs5td7E0xt0FsfOO7C4WQ6YIX2CQIUokPSyRuhqBa9WhufqlReGjLIDT5NbzmF7Yq2BY1pEcDOGJecFIjz1VnL5TeJU1Zg1lSgm2hTh63yy%2Byrn4aoblyjDXg2PG7pZj9UDTU1WQ%2Bugyodz5DY3EGc5ykxG7OMIuy50Jcc73l8mZ9gu9jqYXoR1UUoOxGqs82twnuxTcyWt%2BfHd%2FAh7AMGKYR5r%2BRplIPnzIr17dFZX5LtzGi8h%2F%2BPNLojoD1VO5eQOfLipyvcLCFxvermpgMtT12H7349kSKQLUWgrleA7wbwLHQJTDYEiuri9lm3VSspTXpoUz5oIXkVWIodR65Vgh%2BEiiymUiafvR%2BIcPBe48brKcFv66NfpBGD95yNb0NPdi72kbhxH8UQ3L0nJADblAtb5hO9b%2BVRbcKc45WriB3bcdScC0T2JtEaF%2FFvReBWm7DEEHlBQ44ZqscH%2BBTE2WrOhmmn21%2BMK8%2BCbWb0XcAa%2BGrMMC4tV2y%2FegIjMfH9e66UxzASMqvsqMiOLMVS2rb2vGnnNRjMLy9kurOpnqjNUoJr2KQ%2Fz75UwSBG3O%2BKdebBTdolfRrTkCwiZ4%2BwY4%2FBJdeuQxVsQJNbttsUYo%2B1FQx7CQc1UhG52peeIdkiEKEalFwUtynHB90S62uoBkTlr1fFqWrqezkwxigLQ5qmqXjXO0jGN4jvIgMYBM4HEH2%2F488IBu97KFBf6yxqsZjB4AEzW53m2BNrfdPj09TYI1LAD2tFi9bZZPf5lXQKUCwsRENfQnbzcP4qd8oT5N0W2JcvgChu%2FDFOynDSBb9BT5G6DaAA3J7W9%2FLHpYdh6ZvJeM%2Frp4vnKmQotHIXKIOn3XKQh1Wp12aZl9RyNRWmgWfxAszZ9MZlGNBo8DVrbzq6ZEudxiv2pplKNOHErlSWkpUFpdWYSORqs9wv3XS%2BuPagos8MZblFv%2BZjkcstU8KwISbJejtlNtHBRpnYdqnDrRRq%2FRL7nEXQIKbZx4WSlKNxMnb8A2CDdfTflz5%2B%2Fge%2Bp9SMys4B3ssL1S5UWawClYxJXhtdGgTWWYEGz%2FR9F3k9F5%2F17l3%2FOm0yC%2B%2BRNcA9N6P3vP3716cZqLat1FS6%2BiWEm1IkJjly17p94rt1QVCrvUaEGalix2iSpwdTDlydXK1HJoThVayR%2BJWcU2QZyOxgEWalcaFla7UtF7h%2FMwGxykU5aMi1nCUtM5kQxaH4srx3PD6wrBMe1mkn9lRqd78Ho53g5UAuZUKNdkhLsiUGKnFiiK4yn03OOmJe3Fg9xkBLnWknuSQDHOcAWF1qoKBn%2FHPrxcyBuyk%2Fcq1xe%2Bx5Svl5RmbJ5ifQn2zDfZiU67jHTWvaKteHXTxFzZOuM6ImGMF7wgjqapcOWLgrSqvIcq4kLTH9irqx0JE9vFJxc3nrDWhyB6IlKLBTFu4kG63YLcojIdc7qv5DdbedttMEtA4EUx2VxZpFuELEwIIqbi8xxexAy%2FmqNLUNuxKMXqtVvIZ8EN0rqORGHUoD%2BHd1xSIW281zJW%2FmwXBTFfBSuRgQr0eBEGS6NW8xOFkr0ynpw4utKqGNYHvNQ4JS17Enm7OXi%2FqaG8yHiQVqLrK%2B2rlebjhhEZ6yBuauoVPZSoXGihwihLm16h1uhq5DImt7AC%2FGOzH3uSIKgTsYCm8z4Nf8L%2BIaCSJ0zDaO5HV6A5HcAL2GiDLAEndytsvPk8vyNvFZevcxoajtez6G0TB01JKXiVn5a9JtsIdH3dXw%2BG2Z%2FDZh6wiuZfZNt4Eb5pVK6zhkPcNB2hYC6%2FCmBoV2NWz8f2jhu63MRBhu3u6MjP1s%2FvGw1GNl%2FZWBh02XrZWE0vWy3SWAHcPetSdGiJZQSrDygiZrxLGuEQbBqT4aipxnFCHZZPIKwKluDiSMzS06YooHDxa%2FZH%2BDA7tTEnJkB5VK7%2FaXjwh09B%2FNsOjFIZzM5BJKT88CZSYTMJ8NgiCKeBwHqbyb3%2F8dffg3Xd%2Bb%2FHyhqnUXoYZA2aVNG2%2BDCCded5xAd4Ypko5w67%2BGDrDoP0kNTja1WAOGmUNrN59hjWWrml30DDXWYxo9hFv4SLRWNr2lEZnO9xU7zsg%2BkA7qJmG%2BEp9ojksFr4ofgH7zZxcopDVrj0d7%2BS%2FIHEj0%2BR9%2BytvezTePL5IohcBJG6uGmbxYyB0sJakkJokRmNHTDHa7kdEIGOlm4IyWGY1z7SlD%2Bi2dIHqGM5gJpPw%2Be4%2BgzFnPe5nXzeTf1o7cf%2BRZG97B%2B8Rw3R9w9aOTN5%2B4dG7h%2B%2F307uBw%2BP91%2BHj1%2Fvx8QE%2FsKnOjcQGTQDm3KFZrugTLm07HIVnSrZzQBi1y3XVqRFyRdr1%2B0j5nmOzFN7LcfIo3hD2THNRN644Za7YI18V00N51borFjBVexUCwtq1pBzrnJs%2BB2qk0X8V5a6O%2FYGREe5cdY6y7lR%2BzhrkqOWl2lVhkgd%2BsmVxx%2F%2Bz7uCapNHclWnI3HZJl48UmdMDSGTTLB0lb0rvKVD1fPTLC%2B4OxAp0BHcOYYuCHcmwXfx%2FBfujADxyGQ4CvNMkdkRvKmKKwpwZFdEsbcOIM4iAdYd8fg95depmoIlAeNKDaswSu61qs4EQV5ZtHJTr4S0ox57B6KKXNHSEHymsMB6JIAtYNK5iQZX1JJpxw9IVJNRdtwhgpWXfWNjVnGBj%2ByhmxqzWCcin1muUpytk5NBxOTCnyHs3GbN7dvlFEREhiK9VLdPKQKoSisgpOp1ZSC7Fd6ZG4KvB7efH3r5WSzj%2B%2BFvg9vHfcv9%2BNPXL4NHcT6nPyqs1PcPXBEklWv7hJV6rzXLKt7RZLvPVx47Qzb7WnlBmOSCUGnx2qq0ClGqQbONkDFO478fx%2Fe3A3gY0N2XwT%2FjEgjOuUaqlh8Nw2vW5gBIPUOUtoOgjt8bO3z0V%2F4MZiwpt378Gkbfu8aUJmOrWEqBJYvEdXW99SwSE6%2FFYlHcZy3XRKXJiO8Ak18fHsCIlE9e7L96fLUELoCsBqRJKaTYLiDzk4feRaUW3rnpikXM1LGDlnJlitsiVt%2BVqJJvplHxJP6xSS42xGfyvUBYCIRN3BLbHMJEV9IgjJ7EPzbJEKblhlwgLBnCeVTA8RAmupIGYfQk%2FrHJhTBCbGcgfCgw6J1CmIhK0XWn7xZeZjM88%2FYrCNzkYy2jb%2Bn7fyIGLRf1CjqwtKPOvxa5%2BPHOv3Loo2OyoY7syUB1Y%2FOTSRU2WYWbO%2BNPQmOWWxWcRWU7TxAKrNDtSIE1f2FtLP6yvrD24RskQe4khbL3Ra5t%2BVWuj4nYQQA%2FIZzlcOnu1YlXNRRv02aheK26%2BE%2Bn7baDuyR3FZltM4fq%2BKEuIedyylpFeoaDoZViwNVQuE4rxwbpJxFAmxw%2FcI5CK34qjKogWYxbaFWsstru2lhPomRW4kG1J99oR12f00Quh36nwS%2FFI60vJ2Ae5V5TsOjR0x%2BBiaSy9wbKr9skdf3GW3sL%2FyU9nbIJOFup9dzgV4p5cINbpOaWD2az%2BqIBrNUCKy6lE69Zyv3%2BhMzCTVRadI%2FW4LfGdSn8HGTtXU7qrOLqqsHA1WmhhbhfXGBkIY2tV7s66nKMRAjG9KxlpW%2FVWD2oB0zyzmb9mY8aozjekieQMBAf4cy267qSnYuJiHJBIysala6hEVMiWd0VNDQq5a5Y%2FdLi0Mhy%2FNyp0Cj33MPO4ql5tJmFbb6qfnTGb9WT1IpBs4%2BtnWgzk6%2FkwiVUR8gGrapCAh24OxYFb%2FK5BkeoA%2BuwJSP%2FPcVZntmhjqZdNtpaKAeHu4ZDXUeCEG9a9OfwjksypGlW49NCusV0%2FbbqQSiYUKo6Jd6HDkvnrw7B2bGww9CJ55plbixk2JKRz2fDuIRrNkE%2BUXbMtQwhYgxvx8KkdOK5rsIhxjAOWy7yLT57yQX5TfzijtbHKqPkFfT4y52xdCYI4a5b%2Fawm45MMZT5jy0V8aSS%2B4DWoNLOsujVl4rwdCxNfiOdqdRIL20glg127gF022IlagZppisA6b7%2BCoE4%2BVj9sVGQcp2Sgd8%2FCeHZAJ%2Bq2aaYtAui8%2FYqythCPzVyuR45TMtC7V3vg7IBOVA9UdVftGwJ0UN6ORYkvxHMN1e6rzDoo47AlI797pvTzQ75hK33HwaxyAorScvYrzoXE8tgjRy0Z9h0vlXsghqBBwgPvuqnNBssrPMo%2FFKJsoXatpqm4Kh6QYrpsjivu5YGfGa%2FaNZlkuq4ceYNSU03EwYfEewOiu%2BRV2T0n2NlFNBDY0XVXhCeAt19BmxH5WMtk9wMwDloy6rvmADtD1NMs43ZTqDN1JtENULc9HBqfXCjbNDcAX9aMScvFEHze5ufxPwIzhU7wA%2FIkmKhhWgf%2Fr5SXDaYfyJNKD2ZfT7fZ%2BeySm%2B79f3f%2BFhJgsgJctfXnd7Vp5MXehSjFpgd%2FtouCGLLy8fo5BPtGmp146nG9o6ZJEPmvHtxVjslIK0g7c2%2B7PHikBW%2Bt%2B2JNc%2FDFc%2FLqHRakrMlekEpfsCesCjuvFMVzIgRmTzGRBl3MUjNpR7XmZa%2FE56nZ3XMknZ2Iq9t2Xym8UHEuBARbA1Kh1lC5a9C3KAVP0fBn1eh07GOVLAxfnErSQW%2Fbbnmy8blWG2O%2BQdeCIG8rJGQFDVUy4rvmTDrDgMYkX6c42WblZPM7lBr0LSwWDD9ivg70HIOVjHo%2Bq7X4RNNc7lXPCugWHgKFdv4mUep1XQmLS9cqnlQ9NuvwHbJQ26AiEGa4caoMNzfhTQi%2B%2F3ATTgPQhabcAMy%2FfcQVwPE69qNNFGzhJYNoBjW2WbyL%2FEqNEFtV7%2FzcKx3dz33uVQO9ECtWqaGzKopqoU07WVHewYroaTXnoo38H39stkUDQvp%2FiqsgDqNgvbhARnzBGxSNvQ%2FNc0hbgk4zJUjETJ2H4YIZBszA3mOwOYdwFFeuKtUkpVq4M8qgVE5qG0caE44KZt4v3ltSi%2B6Dt4uXgEhgIuOgAkLhmgq958jbzcH73IcbHaD%2Bx18Aa9JwZSt4qhPlVD1bbRdWbEd9XmAlmoUpUlnYFV5d16CUW24banWVwFPM3O2mq2C7BBeOf%2FiJ7qJ82L7At3UYB88J3ML19iMVWQ9go%2FR7qFr3nzs%2FIUrqDfxV905pIDOxqrEqSp0oK9ztgow8DmzvI9948TJhP8kZsTePt6mffxCAX7xK%2F37wnr0oSA6RhR%2FT0zuHdKzdPPwC6GmVbamKYvVNDFSW0idVv%2FyIm5ZgZROwuvPesvq%2B9%2F7MDzaQU0GgfAvi5TzyXr3Vtgo5j7C867MfbS%2F4EYSffJtTTr%2FNkdbVC1T4oSKX0RgmLopLBA74GIXQ3ri3hwJiLm%2FCuQ%2Bv%2BD8%3D%3C%2Fdiagram%3E%3C%2Fmxfile%3E) or from the file: web/assets/architecture.jpeg 

## Database

The project uses a relational database (MySQL) to persist clean, categorized SMS transactions.  
* Normalized tables: `User`, `Transaction`, `TransactionParticipant`  
* ETL handles creation and upsert operations  
* REST API performs queries and updates efficiently  
* DB files in `database/`, ETL logs in `data/logs/`  
* Provides data integrity, fault tolerance, and scalability  

## API Server

* Located in `api/server.py`  
* Supports CRUD for transactions with Basic Auth protection  
* Returns JSON responses with proper HTTP status and error info

## DSA Comparison

* Script at `dsa/compare_dsa_search.py`  
* Compares linear search vs dictionary lookup on transaction IDs  
* Outputs timing and reflection on efficiencies

## Development Workflow

Agile Scrum tracked on Jira:  
[View Scrum Board](https://alustudent-team1.atlassian.net/jira/software/projects/MSPE/boards/34?atlOrigin=eyJpIjoiYjg2ZjViOGNhM2FhNDUzNmFhZDg1MzA5OTdlOGU3ZmMiLCJwIjoiaiJ9)  
Columns: To Do, In Progress, Done

## Environment

This project was developed and tested on:  
<!-- ubuntu -->
<a href="https://ubuntu.com/" target="_blank"> <img height="" src="https://img.shields.io/static/v1?label=&message=Ubuntu&color=E95420&logo=Ubuntu&logoColor=E95420&labelColor=2F333A" alt="Suite CRM"></a> <!-- bash --> <a href="https://www.gnu.org/software/bash/" target="_blank"> <img height="" src="https://img.shields.io/static/v1?label=&message=GNU%20Bash&color=4EAA25&logo=GNU%20Bash&logoColor=4EAA25&labelColor=2F333A" alt="terminal"></a> <!-- python--> <a href="https://www.python.org" target="_blank"> <img height="" src="https://img.shields.io/static/v1?label=&message=Python&color=FFD43B&logo=python&logoColor=3776AB&labelColor=2F333A" alt="python"></a> </a> <!-- vim --> <a href="https://www.vim.org/" target="_blank"> <img height="" src="https://img.shields.io/static/v1?label=&message=Vim&color=019733&logo=Vim&logoColor=019733&labelColor=2F333A" alt="Suite CRM"></a> <!-- vs code --> <a href="https://code.visualstudio.com/" target="_blank"> <img height="" src="https://img.shields.io/static/v1?label=&message=Visual%20Studio%20Code&color=5C2D91&logo=Visual%20Studio%20Code&logoColor=5C2D91&labelColor=2F333A" alt="Suite CRM"></a> </a><!-- git --> <a href="https://git-scm.com/" target="_blank"> <img height="" src="https://img.shields.io/static/v1?label=&message=Git&color=F05032&logo=Git&logoColor=F05032&labelColor=2F333A" alt="git distributed version control system"></a> <!-- github --> <a href="https://github.com" target="_blank"> <img height="" src="https://img.shields.io/static/v1?label=&message=GitHub&color=181717&logo=GitHub&logoColor=f2f2f2&labelColor=2F333A" alt="Github"></a>
 <!-- Style guidelines -->
* Style guidelines:
  * [pycodestyle (version 2.7.*)](https://pypi.org/project/pycodestyle/)
  * [PEP8](https://pep8.org/)

## Team

<details>
<summary>Monica Dhieu -- Backend & ETL Pipeline Lead</summary>
<ul>
<li><a href="https://github.com/m-dhieu">Github</a></li>
<li><a href="https://www.linkedin.com/in/monica-dhieu">LinkedIn</a></li>
<li><a href="mailto:m.dhieu@alustudent.com">e-mail</a></li>
</ul>
</details>

<details>
<summary>Janviere Munezero -- Database & API Integration</summary>
<ul>
<li><a href="https://github.com/Janviere-dev">Github</a></li>
<li><a href="https://www.linkedin.com/in/munezero-janviere-a5375b300">LinkedIn</a></li>
<li><a href="mailto:janviere.munezero@example.com">e-mail</a></li>
</ul>
</details>

<details>
<summary>Thierry Gabin -- Frontend & Data Visualization</summary>
<ul>
<li><a href="https://github.com/tgabin1">Github</a></li>    
<li><a href="mailto:thierry.gabin@example.com">e-mail</a></li>
</ul>
</details>

<details>
<summary>Santhiana Kaze -- DevOps & Monitoring</summary>
<ul>
<li><a href="https://github.com/ksanthiana">Github</a></li>    
<li><a href="mailto:santhiana.kaze@example.com">e-mail</a></li>
</ul>
</details>

## Setup Instructions

**Prerequisites:**  
* Python 3.8 or newer  
* Virtual environment (optional but encouraged)  
* Bash or compatible command-line  
* Git version control  
* MySQL Server installed and running  
* Python MySQL connector: run `pip install mysql-connector-python`

**Setup:**  
* Clone the repo  
* Run `pip install -r requirements.txt` to install dependencies
* Move to dsa/ and run `python3 parse_xml.py` to process and save clean json data
* Move to project root and run `python3 api/server.py` to start backend server
* From a new terminal move to project root and run `python3 -m http.server -d web/ 3000` to start frontend server
* Interact with visualized data in the frontend dashboard (Username: admin, Password: password)
* Test endpoints in terminal as instructed in `docs/api_docs.md`
* Create `.env` for database connection strings if needed  
* Create your MySQL database and initialize schema:

```
mysql -u your_user -p momo_db < database/database_setup.sql
```

**Current Functionalities:**  
* Parse raw XML data with `dsa/parse_xml.py`  
* Load parsed transactions into JSON `data/processed/transactions.json`  
* Load parsed transactions into MySQL DB via `etl/load_db.py`  
* REST API on `api/server.py` with endpoints  
* DSA performance test in `dsa/compare_dsa_search.py`
* Frontend dashboard for detailed analytics in web/

**Coming Soon:**   
* Automated ETL orchestration and monitoring  

## Contributing

Consult `CONTRIBUTING.md` for guidelines on contributing.

## License

MIT License.

## Contact

Reach out to any listed team member for support, queries, or feedback.

---

*Thursday, November 6, 2025*
