"""
연락처 테이블 생성
"""
CREATE TABLE IF NOT EXISTS "contact"
(
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "profile_url" varchar(200) NULL,
    "name" varchar(100) NOT NULL,
    "email" varchar(254) NULL,
    "phone" varchar(30) NULL,
    "company" varchar(100) NULL,
    "position" varchar(100) NULL,
    "memo" text NULL,
    "address" varchar(255) NULL,
    "birthday" date NULL,
    "website" varchar(200) NULL,
    "created_at" datetime NOT NULL DEFAULT (datetime('now', 'localtime')),
    "updated_at" datetime NULL DEFAULT (datetime('now', 'localtime'))
);

"""
연락처 라벨 테이블 생성
"""
CREATE TABLE IF NOT EXISTS "label"
(
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" varchar(100) NOT NULL
);

"""
연락처와 라벨 간의 다대다 관계 테이블 생성
"""
CREATE TABLE IF NOT EXISTS "contact_label" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "contact_id" BIGINT NOT NULL REFERENCES "contact" ("id") DEFERRABLE INITIALLY DEFERRED,
    "label_id" BIGINT NOT NULL REFERENCES "label" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("contact_id", "label_id"),
    FOREIGN KEY ("contact_id") REFERENCES "contact" ("id") ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY ("label_id") REFERENCES "label" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);