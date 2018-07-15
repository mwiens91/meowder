# ^._.^= ∫ – meowder

meowder is a dating site for cats written with Django, JavaScript, HTML,
and CSS! It is currently hosted at [meowder.com](https://meowder.com).
At its present state, meowder is seeded with fake users, cats, and
votes—so if you want to poke around you'll have some other cats to rate
(although they won't rate your cats back without admin intervention).

## Let me see!

Click [here](https://photos.app.goo.gl/blGCEvfVaTv7Nb202) see an image
set for meowder!

## Let me host!

First copy [`.env.example`](.env.example) to `.env` and fill in
environment variables appropriate for your locale.

Then, like any Django project, migrate

```
./manage.py migrate
```

create a superuser

```
./manage.py createsuperuser
```

run the server

```
./manage.py runserver
```

and point your browser to one of the hosts specified in your `.env`.

Optionally, seed the database with users, cats, and votes with

```
./manage.py seed_database size
```

where size is either `small`, `medium`, or `large`.
