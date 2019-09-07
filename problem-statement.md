You are given a dataset containing data about football players getting transferred across 
various teams/clubs.

Each json record looks like the below. We have players, from and to clubs, and the transfer itself.

```
{
   "season":"2019/2020",
   "player":{
      "href":"/antoine-griezmann/profil/spieler/125781",
      "name":"Antoine Griezmann",
      "position":"Centre-Forward",
      "age":"28",
      "image":"https://tmssl.akamaized.net//images/portrait/medium/125781-1533626871.jpg?lm=1533626889",
      "nationality":"France"
   },
   "from":{
      "href":"/atletico-madrid/startseite/verein/13",
      "name":"Atl\u00e9tico Madrid",
      "country":"Spain",
      "league":"LaLiga",
      "leagueHref":"/primera-division/transfers/wettbewerb/ES1",
      "image":"https://tmssl.akamaized.net//images/wappen/tiny/13.png?lm=1519120744"
   },
   "to":{
      "href":"/fc-barcelona/startseite/verein/131",
      "name":"FC Barcelona",
      "country":"Spain",
      "league":"LaLiga",
      "leagueHref":"/primera-division/transfers/wettbewerb/ES1",
      "image":"https://tmssl.akamaized.net//images/wappen/tiny/131.png?lm=1406739548"
   },
   "transfer":{
      "href":"/jumplist/transfers/spieler/125781/transfer_id/2552096",
      "value":"\u00a3108.00m",
      "timestamp":1563058800
   }
}
```


Your task is to 
1. Find the top 10 player transfers by value. Please note that the value has been given in GBP(Using the pound symbol \u00a3) and in k/m instead of full thousands or lacs value.
2. Find the team with maximum incoming transfers
3. Find the team with maximum outgoing transfers

You will have to ensure that your code filters our any gibberish data that you think should not be considered while solving the above queries.

You code should demonstrate
1) Your programming and design skills
2) Your command over the language
