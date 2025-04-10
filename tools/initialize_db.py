from pathlib import Path

import duckdb

db_path = Path("assets/palworld.duckdb")
con = duckdb.connect(db_path)

# pals(パルの基本情報)
con.execute("""
CREATE TABLE pals (
    pal_id INTEGER PRIMARY KEY,
    name TEXT,
    number INTEGER,
    description TEXT,
    element_type TEXT,
    size TEXT,
    rarity TEXT,
    hp INTEGER,
    melee_attack INTEGER,
    attack INTEGER,
    defense INTEGER,
    work_speed INTEGER,
    support INTEGER,
    capture_rate REAL,
    male_probability REAL,
    egg_type TEXT,
);
""")
comments = [
    ("pal_id", "パルごとのユニークID"),
    ("name", "パルの名前"),
    ("number", "パルの図鑑番号"),
    (
        "element",
        "パルの属性。無属性、炎属性、水属性、雷属性、地属性、草属性、氷属性、竜属性、闇属性のいずれかの値を取る",
    ),
    ("description", "パルに関する説明文"),
    ("size", "パルのサイズ。XS、S、M、L、XLのいずれかの値を取る"),
    (
        "rarity",
        "パルのレアリティ。コモン、レア、エピック、レジェンダリーのいずれかの値を取る",
    ),
    ("hp", "パルのヒットポイント"),
    ("attack", "パルの攻撃力(ATK)"),
    ("defense", "パルの防御力(DEF)"),
    ("work_speed", "パルの作業効率"),
    ("egg_type", "このパルが生まれる卵の種類"),
]
for column_name, comment in comments:
    con.execute(f"COMMENT ON COLUMN pals.{column_name} IS '{comment}';")

# work_suitabilities(作業適性)
con.execute("""
CREATE TABLE work_suitabilities (
    pal_id INTEGER,
    work_type TEXT,
    level INTEGER,
    FOREIGN KEY(pal_id) REFERENCES pals(pal_id)
);
""")

# partner_skills(パートナースキル)
con.execute("""
CREATE TABLE partner_skills (
    pal_id INTEGER,
    skill_name TEXT,
    description TEXT,
    FOREIGN KEY(pal_id) REFERENCES pals(pal_id)
);
""")

# active_skills(アクティブスキル)
con.execute("""
CREATE TABLE active_skills (
    pal_id INTEGER,
    skill_name TEXT,
    element TEXT,
    required_level INTEGER,
    cooldown INTEGER,
    power INTEGER,
    accumulation INTEGER,
    description TEXT,
    FOREIGN KEY(pal_id) REFERENCES pals(pal_id)
);
""")

# passive_skills(パッシブスキル)
con.execute("""
CREATE TABLE passive_skills (
    pal_id INTEGER,
    skill_name TEXT,
    description TEXT,
    FOREIGN KEY(pal_id) REFERENCES pals(pal_id)
);
""")

# drop_items(ドロップアイテム)
con.execute("""
CREATE TABLE drop_items (
    pal_id INTEGER,
    item_name TEXT,
    quantity_range TEXT,
    drop_probability REAL,
    FOREIGN KEY(pal_id) REFERENCES pals(pal_id)
);
""")

# spawn_locations(出現場所)
con.execute("""
CREATE TABLE spawn_locations (
    pal_id INTEGER,
    location TEXT,
    level_range TEXT,
    FOREIGN KEY(pal_id) REFERENCES pals(pal_id)
);
""")

con.close()

print("🎉 DuckDBファイル 'paldex.duckdb' を作成して、テーブルも全部作ったで〜！")

# コメント追加（pals）
comments = [
    ("pals", "pal_id", "パルごとのユニークID"),
    ("pals", "name", "パルの名前"),
    ("pals", "zukan_number", "図鑑番号"),
    ("pals", "element_type", "属性（例：火、氷など）"),
    ("pals", "size", "サイズ（例：XS〜XL）"),
    ("pals", "rarity", "レアリティ（高いほど珍しい）"),
    ("pals", "hp", "ヒットポイント"),
    ("pals", "melee_attack", "近接攻撃力"),
    ("pals", "attack", "遠隔攻撃力"),
    ("pals", "defense", "防御力"),
    ("pals", "work_speed", "作業速度（効率）"),
    ("pals", "support", "サポート力"),
    ("pals", "capture_rate", "捕獲率補正"),
    ("pals", "male_probability", "オスの出現確率（%）"),
    ("pals", "egg_type", "産むタマゴの種類"),
    ("pals", "description", "説明文"),
    ("pals", "image_url", "画像URL"),
]

for table, column, comment in comments:
    con.execute(f"COMMENT ON COLUMN {table}.{column} IS '{comment}';")

# === work_suitabilities ===
con.execute("""
CREATE TABLE work_suitabilities (
    pal_id INTEGER,
    work_type TEXT,
    level INTEGER,
    FOREIGN KEY(pal_id) REFERENCES pals(pal_id)
);
""")

con.execute("COMMENT ON COLUMN work_suitabilities.pal_id IS '対応するパルのID';")
con.execute(
    "COMMENT ON COLUMN work_suitabilities.work_type IS '作業の種類（例：発電、採掘など）';"
)
con.execute("COMMENT ON COLUMN work_suitabilities.level IS '作業レベル（0〜4）';")

# === partner_skills ===
con.execute("""
CREATE TABLE partner_skills (
    pal_id INTEGER,
    skill_name TEXT,
    description TEXT,
    FOREIGN KEY(pal_id) REFERENCES pals(pal_id)
);
""")

con.execute("COMMENT ON COLUMN partner_skills.pal_id IS '対応するパルのID';")
con.execute("COMMENT ON COLUMN partner_skills.skill_name IS 'パートナースキルの名前';")
con.execute("COMMENT ON COLUMN partner_skills.description IS 'スキルの説明文';")

# === active_skills ===
con.execute("""
CREATE TABLE active_skills (
    pal_id INTEGER,
    skill_name TEXT,
    element TEXT,
    required_level INTEGER,
    cooldown INTEGER,
    power INTEGER,
    accumulation INTEGER,
    description TEXT,
    FOREIGN KEY(pal_id) REFERENCES pals(pal_id)
);
""")

active_comments = [
    ("pal_id", "対応するパルのID"),
    ("skill_name", "アクティブスキルの名前"),
    ("element", "スキルの属性"),
    ("required_level", "習得レベル"),
    ("cooldown", "クールダウン時間（秒）"),
    ("power", "スキルの威力"),
    ("accumulation", "状態異常蓄積値"),
    ("description", "スキルの説明文"),
]

for col, comment in active_comments:
    con.execute(f"COMMENT ON COLUMN active_skills.{col} IS '{comment}';")

# === passive_skills ===
con.execute("""
CREATE TABLE passive_skills (
    pal_id INTEGER,
    skill_name TEXT,
    description TEXT,
    FOREIGN KEY(pal_id) REFERENCES pals(pal_id)
);
""")

con.execute("COMMENT ON COLUMN passive_skills.pal_id IS '対応するパルのID';")
con.execute("COMMENT ON COLUMN passive_skills.skill_name IS 'パッシブスキルの名前';")
con.execute("COMMENT ON COLUMN passive_skills.description IS 'パッシブスキルの説明';")

# === drop_items ===
con.execute("""
CREATE TABLE drop_items (
    pal_id INTEGER,
    item_name TEXT,
    quantity_range TEXT,
    drop_probability REAL,
    FOREIGN KEY(pal_id) REFERENCES pals(pal_id)
);
""")

con.execute("COMMENT ON COLUMN drop_items.pal_id IS '対応するパルのID';")
con.execute("COMMENT ON COLUMN drop_items.item_name IS 'ドロップアイテム名';")
con.execute(
    "COMMENT ON COLUMN drop_items.quantity_range IS 'ドロップ個数の範囲（例：1–3）';"
)
con.execute("COMMENT ON COLUMN drop_items.drop_probability IS 'ドロップ確率（%）';")

# === spawn_locations ===
con.execute("""
CREATE TABLE spawn_locations (
    pal_id INTEGER,
    location TEXT,
    level_range TEXT,
    FOREIGN KEY(pal_id) REFERENCES pals(pal_id)
);
""")

con.execute("COMMENT ON COLUMN spawn_locations.pal_id IS '対応するパルのID';")
con.execute("COMMENT ON COLUMN spawn_locations.location IS '出現マップの識別名';")
con.execute(
    "COMMENT ON COLUMN spawn_locations.level_range IS '出現レベルの範囲（例：Lv.1–5）';"
)
