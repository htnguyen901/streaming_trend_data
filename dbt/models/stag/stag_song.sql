with source as (
    select id, title, artist, duration, popularity, timestamp as played_at, created_at,
            features::json
    from {{ ref('recently_played')}} r
),

final as (
    select id, title, artist, duration, popularity, played_at, created_at,
            features->'danceability' as danceability,
            features->'energy' as energy,
            features->'key' as key,
            features->'loudness' as loudness,
            features->'mode' as mode,
            features->'speechiness' as speechiness,
            features->'acousticness' as acousticness,
            features->'instrumentalness' as instrumentalness,
            features->'liveness' as liveness,
            features->'valence' as valence,
            features->'tempo' as tempo,
            features->'time_signature' as time_signature
    from source
)

select * from final