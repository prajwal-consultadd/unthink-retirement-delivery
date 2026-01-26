from db.normalizers import (
    clean_null,
    clean_int,
    clean_bool,
    clean_json,
)

def normalize_linkedin_post(raw: dict) -> dict:
    return {
        "urn": raw.get("urn"),

        "text": clean_null(raw.get("text")),
        "url": clean_null(raw.get("url")),

        "posted_at_timestamp": clean_int(raw.get("postedAtTimestamp")),
        "posted_at_iso": clean_null(raw.get("postedAtISO")),

        "time_since_posted": clean_null(raw.get("timeSincePosted")),
        "is_repost": clean_bool(raw.get("isRepost")),

        "author_type": clean_null(raw.get("authorType")),
        "author_profile_url": clean_null(raw.get("authorProfileUrl")),
        "author_profile_id": clean_null(raw.get("authorProfileId")),
        "author_headline": clean_null(raw.get("authorHeadline")),
        "author_name": clean_null(raw.get("authorName")),

        "type": clean_null(raw.get("type")),
        "share_urn": clean_null(raw.get("shareUrn")),

        "attributes": clean_json(raw.get("attributes")),
        "comments": clean_json(raw.get("comments")),
        "reactions": clean_json(raw.get("reactions")),

        "num_shares": clean_int(raw.get("numShares")),
        "num_likes": clean_int(raw.get("numLikes")),
        "num_comments": clean_int(raw.get("numComments")),

        "can_react": clean_bool(raw.get("canReact")),
        "can_post_comments": clean_bool(raw.get("canPostComments")),
        "can_share": clean_bool(raw.get("canShare")),
        "commenting_disabled": clean_bool(raw.get("commentingDisabled")),

        "allowed_commenters_scope": clean_null(raw.get("allowedCommentersScope")),
        "root_share": clean_bool(raw.get("rootShare")),
        "share_audience": clean_null(raw.get("shareAudience")),

        "author": clean_json(raw.get("author")),
        "author_profile_picture": clean_null(raw.get("authorProfilePicture")),
        "author_urn": clean_null(raw.get("authorUrn")),

        "document": clean_json(raw.get("document")),
        "is_activity": clean_bool(raw.get("isActivity")),
        "input_url": clean_null(raw.get("inputUrl")),
        "linkedin_video": clean_json(raw.get("linkedinVideo")),

        "author_followers_count": clean_int(raw.get("authorFollowersCount")),

        "poll": clean_json(raw.get("poll")),
        "article": clean_json(raw.get("article")),
        "reshared_post": clean_json(raw.get("resharedPost")),

        "activity_description": clean_null(raw.get("activityDescription")),
        "images": clean_json(raw.get("images")),
        "image": clean_json(raw.get("image")),
    }
