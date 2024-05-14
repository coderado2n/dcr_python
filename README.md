# Digital Control Room - Python Test

Thomas Lee's Python code for DCR

## Introduction

I've implemented all the requirements of this task.

## Project Excecution

```bash
python3 stats_by_region.py
python3 load_data.py
```

## Result

The output result in the console is like this.

```json
{
  "regions": [
    {
      "name": "Asia",
      "number_countries": 50,
      "total_population": 4386254784
    },
    {
      "name": "Europe",
      "number_countries": 53,
      "total_population": 746688182
    },
    {
      "name": "Africa",
      "number_countries": 60,
      "total_population": 1185705747
    },
    {
      "name": "Oceania",
      "number_countries": 27,
      "total_population": 40169837
    },
    {
      "name": "Americas",
      "number_countries": 57,
      "total_population": 990317681
    },
    {
      "name": "Polar",
      "number_countries": 1,
      "total_population": 1000
    }
  ]
}
```

And you'd have json log file in the src directory that shows the changes in the database schema.
