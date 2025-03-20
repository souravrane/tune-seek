from collections import defaultdict, Counter
from models.database import db, find_matching_hashes, get_tune_by_id
from utils.logger import log_function

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
            hash_value = (int(anchor_freq), int(target_freq), int(delta_t))
            hashes.append((hash_value, int(anchor_time)))  # Store with song offset time

    return hashes

def match_fingerprint(audio_hashes):
    """Finds best matching song using hashes and offset times."""
    match_scores = defaultdict(list)

    for query_hash, query_offset in audio_hashes:
        results = find_matching_hashes(query_hash)
        
        for result in results:
            song_id = result["tune_id"]
            song_offset = result["offset"]

            # Compute offset difference
            offset_diff = song_offset - query_offset
            match_scores[song_id].append(offset_diff)

    # Find and return the tune with the highest match score
    highest_match = None
    highest_score = 0

    for song_id, offsets in match_scores.items():
        histogram = Counter(offsets)
        # Get the most common offset and its count
        if histogram:
            most_common = histogram.most_common(1)[0]
            peak_count = most_common[1]
            
            if peak_count > highest_score:
                highest_score = peak_count
                highest_match = song_id
    
    # Return the highest matching tune or None if no matches found
    return get_tune_by_id(highest_match)

