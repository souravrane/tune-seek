from collections import defaultdict, Counter
from models.database import db

def create_hashes(fingerprint, tag_range=5):
    """Creates hashes from fingerprint peaks by pairing anchor points with nearby peaks."""
    hashes = list()

    for i in range(len(fingerprint) - 1):
        anchor_time, anchor_freq = fingerprint[i]

        # Pair with the next peak in the tag range
        for j in range(i + 1, min(i + tag_range, len(fingerprint))):
            target_time, target_freq = fingerprint[j]
            
            # Compute time difference
            delta_t = target_time - anchor_time

            # Create hash
            hash_value = (anchor_freq, target_freq, delta_t)
            hashes.append((hash_value, anchor_time))  # Store with song offset time

    return hashes


def match_fingerprint(audio_hashes):
    """Finds best matching song using hashes and offset times."""
    match_scores = defaultdict(list)

    for query_hash, query_offset in audio_hashes:
        results = db.hashes.find({"hash": query_hash})

        for result in results:
            song_id = result["song_id"]
            song_offset = result["offset_time"]

            # Compute offset difference
            offset_diff = song_offset - query_offset
            match_scores[song_id].append(offset_diff)

    # Find and return the top 5 matching tunes based on the offset score
    matching_tunes = list()

    for song_id, offsets in match_scores.items():
        histogram = Counter(offsets)
        peak_offset, peak_count = histogram.most_common()
        matching_tunes.append([peak_count, song_id])

    matching_tunes.sort()
    return matching_tunes[:5]

