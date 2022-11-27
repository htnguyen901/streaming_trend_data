with source as (
    select id, name, artist, duration, popularity, created_at, genres, playlist,
            features::json
    from {{ ref('tracks_from_playlists')}} r
),

final as (
    select id,
            replace(name, '''', '') as name,
            replace(artist, '''', '') as artist,
            duration, popularity, created_at,
            replace(genres, '''', '') as genres,
            playlist,
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