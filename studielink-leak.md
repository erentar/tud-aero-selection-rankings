---
format:
  html:
    self-contained: true

---

It is possible to get your ranking number at least a week earlier[^studielink-leak-1] if you applied to multiple schools.

[^studielink-leak-1]: perhaps even earlier than that, but the hard evidence we have is for at least a week

# Instructions

1.  Navigate to [studielink](https://www.studielink.nl/) and log in.
2.  Enable devtools (F12 on firefox, Ctrl+Shift+i on chrome)
3.  go to the networking tab
4.  Check "Disable Cache", and enable "Persist Logs"

![](images/clipboard-799079229.png)

5.  Reload the page

6.  In the body of the webpage, in the top header, click on "Payments"

7.  In the networking tab of the devtools pane, there will be a request to `/api/betaling` which returns a json.

8.  The rank may be available at the following path within this json response:

    ``` json
    ["allBetalingen"][#]["inschrijvingenInAndereInstellingen"]["plaatsRangnummerGroep"]
    ```

    where `#` is from 0 up to the length of the list

As you notice, we are getting the value at the path

```         
/allBetalingen/#/inschrijvingenInAndereInstellingen/plaatsRangnummerGroep
```

When translated to english, this becomes

```         
/All Payments/0..n/Registrations in other institutions/Placement rank number group/
```

In the `jq` query language, the keys and values of interest can be obtained with

``` bash
#!/bin/sh

cat betaling.json \
| jq '.["allBetalingen"][] | [ 
        .["instellingNaam"],
        (.["inschrijvingenInAndereInstellingen"][] | [.["id"], .["plaatsRangnummerGroep"]])  ]'
```

which produces an output in the format

``` json
[
  "Delft University of Technology",
  [
    "483dbb45-66ac-41af-b922-d6f233b3a297",
    null
  ],
  [
    "00b7c37a-447e-48a3-843a-ebdf8552c6c1",
    null
  ]
]
[
  "Eindhoven University of Technology",
  [
    "483dbb45-66ac-41af-b922-d6f233b3a297",
    null
  ],
  [
    "39b6f298-9a9e-411f-83cf-d86de79aca01",
    {
      "rangnummer": 672
    }
  ]
]
```

In this example, this student (me) got the ranking number 672 under "Other registrations" from *TU Eindhoven*. This ranking number is not my *TU Eindhoven* ranking number, but in fact is the ranking number I received from another program I applied during the same year as I did for *TU Eindhoven*.

*Course ids* (for example `483db…`, `00b7c…`, `39b6f…`) can be translated to *course names*, although their names are in a separate network request. This request is to `/api/opleiding`. Here, each course is in a list, and have properties of interest `"id"` and `"naam"`.

we can get the information we need by the jq query

``` bash
#!/bin/sh

cat opleiding.json \
| jq '.[] | [ .["id"], .["naam"], .["opleidingsdetails"]["instellingsnaam"] ]'
```

which will yield a response similar to

``` json
[
  "39b6f298-9a9e-411f-83cf-d86de79aca01",
  "Aerospace Engineering - Bachelor",
  "Delft University of Technology"
]
[
  "00b7c37a-447e-48a3-843a-ebdf8552c6c1",
  "Mechanical Engineering (bachelor)",
  "Eindhoven University of Technology"
]
[
  "483dbb45-66ac-41af-b922-d6f233b3a297",
  "Mechanical Engineering - Bachelor",
  "University of Twente"
]
```

The rank number we got from the previous step was for `39b6f…`. Here, we find out that it is the number for Delft Aerospace.

To my knowledge none of the other schools, other than Delft, made this number available in this fashion. If you are seeing any number at all in `/api/betaling`, it is likely it is from Delft. People who applied to both CSE and AE received both their rankings, and the response at `/api/opleiding` will let people know which is which.
