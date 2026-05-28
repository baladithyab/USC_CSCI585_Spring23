-- DB => postgresql on supabase
CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    age INT,
    address VARCHAR(255)
);

CREATE TABLE channels (
    channel_id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    owner_id UUID NOT NULL,
    subscription_count INT DEFAULT 0,
    created_on DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (owner_id) REFERENCES users (user_id)
);

CREATE TABLE subscriptions (
    subscriber_id UUID NOT NULL,
    channel_id UUID NOT NULL,
    subscription_type VARCHAR(20) NOT NULL,
    PRIMARY KEY (subscriber_id, channel_id),
    FOREIGN KEY (subscriber_id) REFERENCES users (user_id),
    FOREIGN KEY (channel_id) REFERENCES channels (channel_id)
);

CREATE TABLE videos (
    video_id UUID PRIMARY KEY,
    url VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    channel_id UUID NOT NULL,
    thumbnail_url VARCHAR(255),
    category VARCHAR(20) NOT NULL,
    keyword VARCHAR(20) NOT NULL,
    tag VARCHAR(20) NOT NULL,
    duration INTERVAL NOT NULL,
    description TEXT,
    uploader_id UUID NOT NULL,
    upload_date date DEFAULT CURRENT_DATE,
    upload_time time DEFAULT CURRENT_TIME,
    FOREIGN KEY (uploader_id) REFERENCES users (user_id),
    FOREIGN KEY (channel_id) REFERENCES channels (channel_id)
);

CREATE TABLE video_statistics (
    video_id UUID NOT NULL,
    likes INT DEFAULT 0,
    dislikes INT DEFAULT 0,
    view_count INT DEFAULT 0,
    share_count INT DEFAULT 0,
    PRIMARY KEY (video_id),
    FOREIGN KEY (video_id) REFERENCES videos (video_id)
);

CREATE TABLE comments (
    comment_id UUID PRIMARY KEY,
    video_id UUID NOT NULL,
    user_id UUID NOT NULL,
    text TEXT NOT NULL,
    likes INT DEFAULT 0,
    sentiment float not null,
    commented_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (video_id) REFERENCES videos (video_id),
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);

CREATE TABLE sponsors (
    sponsor_id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(255),
    address VARCHAR(255)
);

CREATE TABLE sponsored_videos (
    video_id UUID NOT NULL,
    sponsor_id UUID NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (video_id, sponsor_id),
    FOREIGN KEY (video_id) REFERENCES videos (video_id),
    FOREIGN KEY (sponsor_id) REFERENCES sponsors (sponsor_id)
);