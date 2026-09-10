<<<<<<< HEAD
## Online Fundraising Platform — one SDLC cycle, six people

**Six-person group project.** The team split into a
programming team and a documentation team, and I was on the documentation side. **My part: user
stories #37–42; BCE class and sequence diagrams for 14 of the 42 use cases (#27–37 and #40–42); use
case diagrams and descriptions; wireframes; and the Gantt chart.**

The split was not front end versus back end in the usual sense. **The screens came from our side —
the HTML wireframes in `wireframes/` and the Jinja templates in `templates/`. The Python behind them
— routes, controllers, entities — was written by the programming team.**

That is what makes this repository different from the rest of my portfolio. The others are code I
wrote alone. **This one is a record of requirements I defined, screens my side drew, and what the
two became together** — which file, which route, which query, which test.

The signed contribution table in `docs/` records the division as it was agreed. In practice the two
sides crossed it in both directions, which is the subject of *How the team actually worked* below.
=======
## Singapore HDB Resale Price Analysis
>>>>>>> 202d5b3 (Add seeded role accounts to the run steps; point at the report's demo recording)

### Overview

216,375 HDB resale transactions, January 2017 to September 2025, from data.gov.sg.

The project answers four questions a buyer would actually ask:

1. Which towns are the most and least expensive?
2. Does a higher floor actually cost more?
3. Is there really a price cliff once the remaining lease drops below 60 years?
4. Has the gap between towns changed since 2017?

Three of the four turn out to have the same trap in them, which is what the *Method* section
below is about.

### Technical Implementation
* ****Language****: Python
* ****Libraries****: pandas (data manipulation), matplotlib (visualisation)
* ****Tools****: Jupyter Notebook, Power BI

### Key Findings

**1. Town — a 72% gap between the ends.**
Bukit Timah averages $769K, Yishun $447K. This one is safe to read at face value.

**2. Floor — a real premium, but about 15.7% per 10 floors, not 2.6x.**
Grouped by storey range, the top band (49–51) averages 2.6 times the bottom band. That band
holds **19 sales out of 216,375, and all 19 are in one town** — Central Area. It is the most
expensive town in Singapore showing up under a storey label. Holding town, flat type and year
constant, an extra floor is worth about **$87 per sqm, or 15.7% per 10 floors**. The
uncontrolled comparison overstates the effect by **53%**.

**3. Remaining lease — no cliff at 60 years.**
The common view is that prices drop sharply once the lease falls under about 60 years. Among
4-room flats sold in 2024, the line is flat through that mark, and flats with **45–50 years
left sell for more per sqm than flats with 60–75 years left**. Holding the town constant, an
extra lease year is worth **under 1% per sqm** (+0.95% at 45–60 years, +0.41% at 60–75, +0.79%
at 75–95), and the effect does not accelerate below 60. The short leases sit in the oldest, most
central estates, so the town is doing the work again.

**4. Towns are converging.**
The cheapest towns in 2017 grew the fastest: Sembawang +68%, Woodlands +57%, against Central
Area +28% and Bishan +28%. The correlation between a town's 2017 price level and its later
growth is **−0.64**. The ranking barely moved, but the gap between the most and least expensive
town narrowed from **2.36x to 1.97x**.

### So what

Three of these change what a buyer should actually look at.

**Height is worth less than the listings suggest, and only in the right place.** Ten floors is
worth roughly 16% per sqm once the town is held constant. Paying a large premium for a high
floor inside an already expensive town means paying for the location twice — the height is
already in the town price.

**Screening flats by remaining lease alone filters on the wrong variable.** A 45–55 year lease
is not the discount the "60-year cliff" story implies, because those flats sit in mature central
estates and are priced up by that. A buyer avoiding short leases on principle is ruling out
central locations without meaning to.

**If growth matters more than the address, the record points the other way round.** Since 2017
the cheapest towns grew the fastest and the most expensive grew the slowest.

One caveat on the last point: this describes what has already happened. Eight years of one
direction is not a forecast, and the towns that grew fastest were also the ones with the most
room to catch up.

### Method

All three of the interesting findings are the same problem: a difference that looks like it
belongs to one variable actually belongs to the town.

To separate them I compare each sale against the average of its own group (town, flat type and
year) rather than against the whole dataset, so what is left is the within-group difference. It
is a simple approach — a regression with all the variables at once would be stronger — but it is
enough to show that the raw storey and lease numbers are misleading, and by how much.

I also check the sample size of every band before quoting an average from it. That is what
caught the 19-transaction storey band.

### Visualisations

![Price by town](images/price_by_town.png)

Grey bars mark storey bands with fewer than 200 sales — the averages there are not reliable,
and that is where the 2.6x comes from:

![Price per sqm by storey range](images/price_by_floor.png)

![Price per sqm by remaining lease](images/price_by_lease.png)

![Growth by town](images/growth_by_town.png)

### Power BI dashboard

![Power BI dashboard](images/powerbi_dashboard.png)

The dashboard file is `SG_HDB_RESALE.pbix`, exported as `SG_HDB_RESALE.pdf`. GitHub cannot
render `.pbix`, so the image above is the readable version.

The dashboard covers the town comparison only. The storey and lease questions need the
group-mean adjustment described under *Method*, which is done in the notebook.

### Repository Structure

```
singapore-hdb-analysis/
├── Singapore_HDB_Analysis.ipynb                                  # Main analysis notebook
├── ResaleflatpricesbasedonregistrationdatefromJan2017onwards.csv # Dataset
├── images/                                                       # Charts (generated by the notebook)
├── SG_HDB_RESALE.pbix                                            # Power BI file
├── SG_HDB_RESALE.pdf                                             # Dashboard export
└── README.md                                                     # Documentation
```

### How to Run

```bash
# 1. Clone the repository
git clone https://github.com/JinWanKim98/singapore-hdb-analysis.git
cd singapore-hdb-analysis

# 2. Install dependencies
pip install pandas matplotlib jupyter

# 3. Run the notebook
jupyter notebook Singapore_HDB_Analysis.ipynb
```

Running the notebook regenerates every chart in `images/`.

### Limitations

- The comparisons hold town, flat type and year constant, but not flat model, block age or
  distance to an MRT station. Some of what is left may still belong to those.
- Comparing each sale against its own town / type / year average is a simple way to control for
  them. A regression with all the variables at once would be a stronger test.
- 2025 data stops in September, so 2025 is not used in the year-on-year comparison.
- The dataset records what flats sold for, not what they were listed at, so nothing here says
  anything about how long a flat takes to sell.
