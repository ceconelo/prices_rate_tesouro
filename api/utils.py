from typing import List
import inspect
import json


def format_date(date):
    return date.split('T')[0]  # Remove the time from the date


fake_file = {
  "Tesouro Prefixado\t2023-01-01": {
    "date": "2022-06-23",
    "bid": 13.54,
    "ask": 13.66,
    "puc": 935.64,
    "puv": 934.65,
    "txm": 13.6,
    "pum": 935.145
  },
  "Tesouro Prefixado\t2025-01-01": {
    "date": "2022-06-23",
    "bid": 12.42,
    "ask": 12.54,
    "puc": 744.53,
    "puv": 742.18,
    "txm": 12.48,
    "pum": 743.355
  },
  "Tesouro IPCA+\t2024-08-15": {
    "date": "2022-06-23",
    "bid": 6.01,
    "ask": 6.13,
    "puc": 3513.18,
    "puv": 3503.13,
    "txm": 6.07,
    "pum": 3508.155
  },
  "Tesouro IPCA+\t2035-05-15": {
    "date": "2022-06-23",
    "bid": 5.75,
    "ask": 5.87,
    "puc": 1940.55,
    "puv": 1911.65,
    "txm": 5.81,
    "pum": 1926.1
  },
  "Tesouro IPCA+\t2045-05-15": {
    "date": "2022-06-23",
    "bid": 5.75,
    "ask": 5.87,
    "puc": 1111.21,
    "puv": 1082.34,
    "txm": 5.81,
    "pum": 1096.775
  },
  "Tesouro IPCA+ com Juros Semestrais\t2024-08-15": {
    "date": "2022-06-23",
    "bid": 6.05,
    "ask": 6.17,
    "puc": 4060.93,
    "puv": 4049.95,
    "txm": 6.11,
    "pum": 4055.44
  },
  "Tesouro IPCA+ com Juros Semestrais\t2026-08-15": {
    "date": "2022-06-23",
    "bid": 5.59,
    "ask": 5.71,
    "puc": 4121.9,
    "puv": 4103.02,
    "txm": 5.65,
    "pum": 4112.46
  },
  "Tesouro IPCA+ com Juros Semestrais\t2035-05-15": {
    "date": "2022-06-23",
    "bid": 5.72,
    "ask": 5.84,
    "puc": 4109.94,
    "puv": 4065.7,
    "txm": 5.78,
    "pum": 4087.82
  },
  "Tesouro IPCA+ com Juros Semestrais\t2045-05-15": {
    "date": "2022-06-23",
    "bid": 5.88,
    "ask": 6,
    "puc": 4072.26,
    "puv": 4012.06,
    "txm": 5.94,
    "pum": 4042.16
  },
  "Tesouro IPCA+ com Juros Semestrais\t2050-08-15": {
    "date": "2022-06-23",
    "bid": 5.91,
    "ask": 6.03,
    "puc": 4120.59,
    "puv": 4055.11,
    "txm": 5.97,
    "pum": 4087.85
  },
  "Tesouro IGPM+ com Juros Semestrais\t2031-01-01": {
    "date": "2022-06-23",
    "bid": 5.59,
    "ask": 5.71,
    "puc": 9524.22,
    "puv": 9456.88,
    "txm": 5.65,
    "pum": 9490.55
  },
  "Tesouro Prefixado com Juros Semestrais\t2023-01-01": {
    "date": "2022-06-23",
    "bid": 13.54,
    "ask": 13.66,
    "puc": 1030,
    "puv": 1028.93,
    "txm": 13.6,
    "pum": 1029.465
  },
  "Tesouro Prefixado com Juros Semestrais\t2025-01-01": {
    "date": "2022-06-23",
    "bid": 12.49,
    "ask": 12.61,
    "puc": 996.94,
    "puv": 994.16,
    "txm": 12.55,
    "pum": 995.55
  },
  "Tesouro Prefixado com Juros Semestrais\t2027-01-01": {
    "date": "2022-06-23",
    "bid": 12.5,
    "ask": 12.62,
    "puc": 966.65,
    "puv": 962.56,
    "txm": 12.56,
    "pum": 964.605
  },
  "Tesouro Prefixado com Juros Semestrais\t2029-01-01": {
    "date": "2022-06-23",
    "bid": 12.64,
    "ask": 12.76,
    "puc": 938.16,
    "puv": 933.12,
    "txm": 12.7,
    "pum": 935.64
  },
  "Tesouro Selic\t2023-03-01": {
    "date": "2022-06-23",
    "bid": 0.0383,
    "ask": 0.0483,
    "puc": 11813.28,
    "puv": 11806.62,
    "txm": 0.0433,
    "pum": 11809.95
  },
  "Tesouro Selic\t2025-03-01": {
    "date": "2022-06-23",
    "bid": 0.1086,
    "ask": 0.1186,
    "puc": 11781.96,
    "puv": 11772.94,
    "txm": 0.1136,
    "pum": 11777.45
  },
  "Tesouro Prefixado\t2026-01-01": {
    "date": "2022-06-23",
    "bid": 12.35,
    "ask": 12.47,
    "puc": 663.42,
    "puv": 660.62,
    "txm": 12.41,
    "pum": 662.02
  },
  "Tesouro IPCA+\t2026-08-15": {
    "date": "2022-06-23",
    "bid": 5.54,
    "ask": 5.66,
    "puc": 3183.41,
    "puv": 3167.1,
    "txm": 5.6,
    "pum": 3175.255
  },
  "Tesouro IPCA+ com Juros Semestrais\t2030-08-15": {
    "date": "2022-06-23",
    "bid": 5.56,
    "ask": 5.68,
    "puc": 4178.87,
    "puv": 4146.58,
    "txm": 5.62,
    "pum": 4162.725
  },
  "Tesouro IPCA+ com Juros Semestrais\t2040-08-15": {
    "date": "2022-06-23",
    "bid": 5.77,
    "ask": 5.89,
    "puc": 4170.16,
    "puv": 4115.84,
    "txm": 5.83,
    "pum": 4143
  },
  "Tesouro IPCA+ com Juros Semestrais\t2055-05-15": {
    "date": "2022-06-23",
    "bid": 5.92,
    "ask": 6.04,
    "puc": 4060.39,
    "puv": 3991.31,
    "txm": 5.98,
    "pum": 4025.85
  },
  "Tesouro Prefixado com Juros Semestrais\t2031-01-01": {
    "date": "2022-06-23",
    "bid": 12.67,
    "ask": 12.79,
    "puc": 917.15,
    "puv": 911.4,
    "txm": 12.73,
    "pum": 914.275
  },
  "Tesouro Prefixado\t2024-07-01": {
    "date": "2022-06-23",
    "bid": 12.75,
    "ask": 12.87,
    "puc": 786.24,
    "puv": 784.19,
    "txm": 12.81,
    "pum": 785.215
  },
  "Tesouro Selic\t2024-09-01": {
    "date": "2022-06-23",
    "bid": 0.0885,
    "ask": 0.0985,
    "puc": 11793.58,
    "puv": 11785.14,
    "txm": 0.0935,
    "pum": 11789.36
  },
  "Tesouro Selic\t2027-03-01": {
    "date": "2022-06-23",
    "bid": 0.1578,
    "ask": 0.1678,
    "puc": 11729.74,
    "puv": 11718.41,
    "txm": 0.1628,
    "pum": 11724.075
  },
  "Tesouro Prefixado\t2029-01-01": {
    "date": "2022-06-23",
    "bid": 12.55,
    "ask": 12.67,
    "puc": 463.71,
    "puv": 460.29,
    "txm": 12.61,
    "pum": 462
  },
  "Tesouro IPCA+ com Juros Semestrais\t2032-08-15": {
    "date": "2022-06-23",
    "bid": 5.65,
    "ask": 5.77,
    "puc": 4171.08,
    "puv": 4133.32,
    "txm": 5.71,
    "pum": 4152.2
  },
  "Tesouro Prefixado com Juros Semestrais\t2033-01-01": {
    "date": "2022-06-23",
    "bid": 12.7,
    "ask": 12.82,
    "puc": 899.71,
    "puv": 893.45,
    "txm": 12.76,
    "pum": 896.58
  },
  "xlsLastUpdated": "23-06-2022"
}
