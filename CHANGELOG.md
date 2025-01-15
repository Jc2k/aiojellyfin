# CHANGELOG



## v0.12.0 (2025-01-15)

### Feature

* feat: expose all audio_url settings ([`d2b880c`](https://github.com/Jc2k/aiojellyfin/commit/d2b880c926e37c5e663993f451e2bc5e59a12991))

* feat: add options for transcoding ([`6ee2153`](https://github.com/Jc2k/aiojellyfin/commit/6ee21533ef6cf1a77440d2f60ed8b82484a39460))


## v0.11.2 (2025-01-09)

### Fix

* fix: preserve endpoint when cloning builders ([`4c13caa`](https://github.com/Jc2k/aiojellyfin/commit/4c13caa3a5f9101a13765c3832dafd814b9711bb))


## v0.11.1 (2025-01-09)

### Fix

* fix: in_playlist needs to return the clone ([`ed7b46a`](https://github.com/Jc2k/aiojellyfin/commit/ed7b46ad070e0157b42c93aeb777f4b5ae3e466f))


## v0.11.0 (2025-01-09)

### Chore

* chore: more lint config changes ([`8bdf31f`](https://github.com/Jc2k/aiojellyfin/commit/8bdf31fea1bbb5631d0c8aacc38832485701ad7c))

* chore: properly update ruff in extras ([`d8b4bd5`](https://github.com/Jc2k/aiojellyfin/commit/d8b4bd5b4b5e7c6d2c89d0bf25c6d04887068097))

### Feature

* feat: better support for querying playlists ([`e472765`](https://github.com/Jc2k/aiojellyfin/commit/e4727657bccc4a3ebff272cefd2aecd70ded5b5f))

### Fix

* fix: correct ruff config warnings after update ([`f768b80`](https://github.com/Jc2k/aiojellyfin/commit/f768b804de809a7e39eb5ac2b5bc30eb8fbd39b1))


## v0.10.1 (2024-08-24)

### Chore

* chore: lint fixes ([`22b767f`](https://github.com/Jc2k/aiojellyfin/commit/22b767f84e81fdbe764e838c698c89b01c853575))

### Fix

* fix: always use the shared ClientSession ([`4551ff6`](https://github.com/Jc2k/aiojellyfin/commit/4551ff6ba974c890749d40e4e1328cac5a6bdc26))


## v0.10.0 (2024-07-23)

### Chore

* chore: test interupt ([`712e457`](https://github.com/Jc2k/aiojellyfin/commit/712e4578d6c7f90aa5bea0f754e108a7d44ac995))

* chore: cleanup __all__ ([`11f766e`](https://github.com/Jc2k/aiojellyfin/commit/11f766ea6f9158e01fd18f321bbed58b50ddd628))

* chore: fix fixture line endings ([`bcac7ca`](https://github.com/Jc2k/aiojellyfin/commit/bcac7cafeb18ff13f68a419661802f9c70323069))

* chore: tests and mypy passing ([`ac306f7`](https://github.com/Jc2k/aiojellyfin/commit/ac306f7c3e729e148b9870d77832d13fbf1452ae))

* chore: test refactoring to improve mypy coverage ([`a28f2e6`](https://github.com/Jc2k/aiojellyfin/commit/a28f2e634be69127a74e8f1bc3ba6fcbfe63703c))

* chore: update test infra for new builder pattern api ([`73fb5b1`](https://github.com/Jc2k/aiojellyfin/commit/73fb5b182d07ec8589960cae8a3029e9f74f648e))

### Feature

* feat: get_similar_tracks now uses ItemFields enum ([`a0aab85`](https://github.com/Jc2k/aiojellyfin/commit/a0aab85715497c20e3a324e7975c2fa622c540eb))

* feat: add greedy pagination to MediaItemsQueryBuilder.stream() ([`ea69a42`](https://github.com/Jc2k/aiojellyfin/commit/ea69a425823802d96c245933bae118a4821bc583))

* feat: add ItemFields enum ([`204c73e`](https://github.com/Jc2k/aiojellyfin/commit/204c73e01305287683bbe3cf0d64ee1571942a01))

* feat: c.tracks, c.albums, c.artists and c.playlists are now all query builder objects ([`c8d8301`](https://github.com/Jc2k/aiojellyfin/commit/c8d83014a1c6413927bc0122e53620f2622c15d3))

* feat: add builder pattern for querying ([`f64e973`](https://github.com/Jc2k/aiojellyfin/commit/f64e973da4469e632d22cd40c6d7276b74eac19b))

### Unknown

* Merge pull request #1 from Jc2k/builder

Builder pattern for creating Jellyfin queries ([`c775ab4`](https://github.com/Jc2k/aiojellyfin/commit/c775ab4d038833865f003be3fc10deb8adaa0687))


## v0.9.2 (2024-07-22)

### Fix

* fix: make sure all artists are returned ([`2238f5c`](https://github.com/Jc2k/aiojellyfin/commit/2238f5cbb65a9f971bb477c7d9cab2d66f21a0ff))


## v0.9.1 (2024-06-25)

### Fix

* fix: typo in API ([`e4ad38b`](https://github.com/Jc2k/aiojellyfin/commit/e4ad38b6a92f0418b5c201777e1b425bc13c16da))


## v0.9.0 (2024-06-24)

### Chore

* chore: readme update ([`bd6e9c8`](https://github.com/Jc2k/aiojellyfin/commit/bd6e9c8c12bbc5b0420123548c59f395374b1a45))

* chore: lint fixes ([`281b8da`](https://github.com/Jc2k/aiojellyfin/commit/281b8da8612d938928b0573351ba689668a35abd))

### Feature

* feat: add similar tracks ([`78691b5`](https://github.com/Jc2k/aiojellyfin/commit/78691b559872e5c71c1c056403a9957a3dcae18a))

* feat: add suggested tracks endpoint ([`ed0313d`](https://github.com/Jc2k/aiojellyfin/commit/ed0313d993f257af3ae47f3432ca2b34d0ff602e))

### Unknown

* BREAKING CHANGE: removed get_user_items ([`0e42675`](https://github.com/Jc2k/aiojellyfin/commit/0e42675fa0d2413d92bfe5c88cc8e6fb211f91ba))

* BREAKING CHANGE: removed get_item ([`4ed451d`](https://github.com/Jc2k/aiojellyfin/commit/4ed451d18cd0c6e735461bb19c8f7e739e062e05))

* BREAKING CHANGE: removed search_media_items ([`19a5db5`](https://github.com/Jc2k/aiojellyfin/commit/19a5db51e2d2b8d575e419e89428d0885087cd6e))


## v0.8.3 (2024-06-22)

### Fix

* fix: the field AlbumId not present in test fixtures that don&#39;t belong to an album ([`aeac337`](https://github.com/Jc2k/aiojellyfin/commit/aeac3375e6ef732ae9e93191c2d0f766ff449e86))


## v0.8.2 (2024-06-22)

### Fix

* fix: use JSONDecoder when adding fixtures to tests ([`7c089ed`](https://github.com/Jc2k/aiojellyfin/commit/7c089eda6d4bd29d9a50d95cacbefb9b21039482))


## v0.8.1 (2024-06-22)

### Fix

* fix: fix method name typo ([`97fdec0`](https://github.com/Jc2k/aiojellyfin/commit/97fdec00ff6a9a3d9980cb6bae16729e78e3b785))


## v0.8.0 (2024-06-22)

### Feature

* feat: add framework for testing apps using aiojellyfin ([`5edc68e`](https://github.com/Jc2k/aiojellyfin/commit/5edc68ef23a55d1a34a2d05f79c71391b7a5d2da))


## v0.7.0 (2024-06-19)

### Chore

* chore: linters ([`7313357`](https://github.com/Jc2k/aiojellyfin/commit/73133577da84419d6275c3d24b1314bfa8711937))

### Feature

* feat: improve artwork url generator ([`eb289d0`](https://github.com/Jc2k/aiojellyfin/commit/eb289d074f0be95906b3b10853691abacd9287db))


## v0.6.0 (2024-06-19)

### Chore

* chore: move ItemType into new const module ([`e7fab50`](https://github.com/Jc2k/aiojellyfin/commit/e7fab508c258cccb93878b0529ff2f975b3faaa7))

### Feature

* feat: wrap backdrop handling ([`3cca4e6`](https://github.com/Jc2k/aiojellyfin/commit/3cca4e6a06b3ac02af928a21bb17e73175b177d6))


## v0.5.0 (2024-06-19)

### Feature

* feat: make library_id optional and support searching used typed functions ([`e56464a`](https://github.com/Jc2k/aiojellyfin/commit/e56464aae195a831d3a1ad55568c39fee2760d43))


## v0.4.0 (2024-06-19)

### Feature

* feat: add typed helpers for getting a single artist/album/track/playlist ([`8f199c2`](https://github.com/Jc2k/aiojellyfin/commit/8f199c2472f49761713d1a41f54ce19d5b2e277b))


## v0.3.0 (2024-06-18)

### Feature

* feat: adds support for startIndex ([`1c41f6f`](https://github.com/Jc2k/aiojellyfin/commit/1c41f6f6a8941bb8a03e88b9e1984459dd1534e7))

* feat: add &#39;limit&#39; option to more endpoints ([`319baf2`](https://github.com/Jc2k/aiojellyfin/commit/319baf27c2188f9fd2f036dc1dad279fb72312d8))

* feat: add typed endpoint for fetching playlists ([`163694f`](https://github.com/Jc2k/aiojellyfin/commit/163694f048044a667c63530730eea3ba31ade320))

* feat: support listing all tracks in a library ([`f5b2690`](https://github.com/Jc2k/aiojellyfin/commit/f5b2690393624aab9b4dfddcc66b079f93ff1a68))


## v0.2.0 (2024-06-17)

### Chore

* chore: revert previous ci change ([`d6a785a`](https://github.com/Jc2k/aiojellyfin/commit/d6a785ae9b468142b53ff1d6aedf61cf828e1230))

* chore: don&#39;t limit commits on main as it is too late ([`9c2f7ac`](https://github.com/Jc2k/aiojellyfin/commit/9c2f7ac49a0af3677af7ab75c9753853fd596491))

### Feature

* feat: Add albums() that can return all albums in library ([`f6470ab`](https://github.com/Jc2k/aiojellyfin/commit/f6470abc6810d64dd42ac856126279d9f8a41af7))

### Fix

* fix: Set recursive so all albums are found ([`89b78da`](https://github.com/Jc2k/aiojellyfin/commit/89b78da1449644e5be8679778ea7c5464b8dd23e))


## v0.1.0 (2024-06-17)

### Feature

* feat: allow artists() and search_media_items() to set fields and enableUserData on queries ([`f9a528c`](https://github.com/Jc2k/aiojellyfin/commit/f9a528ca06c38b0230fe9b6089c74bbb0e6f8328))


## v0.0.6 (2024-06-17)

### Chore

* chore: ruff format ([`97a6e21`](https://github.com/Jc2k/aiojellyfin/commit/97a6e2124e01a2455f27b5b135747e475baba167))

* chore: ruff check ([`29320a2`](https://github.com/Jc2k/aiojellyfin/commit/29320a2d8967de95532d5acb9104b9d6c534b4fe))

### Fix

* fix: the Artist class should properly subclass MediaItem ([`db597a1`](https://github.com/Jc2k/aiojellyfin/commit/db597a1853034e189fe671375f3f458acfadcfe4))


## v0.0.5 (2024-06-17)

### Chore

* chore: fix spelling ([`63651d2`](https://github.com/Jc2k/aiojellyfin/commit/63651d29ecdba207accc4e2748124f3eb791a6fa))

### Fix

* fix: added more typing information ([`8cc3eb5`](https://github.com/Jc2k/aiojellyfin/commit/8cc3eb50e078b0c9e31dbfc6a6c463b8f361d457))


## v0.0.4 (2024-06-14)

### Fix

* fix: build wheels before releasing to pypi ([`c790e28`](https://github.com/Jc2k/aiojellyfin/commit/c790e281488ac9112a39e59d3c83a3df2c07c6cb))


## v0.0.3 (2024-06-14)

### Fix

* fix: remove stray conditional in release pipeline ([`54f5ecf`](https://github.com/Jc2k/aiojellyfin/commit/54f5ecfb85a14c8f6a01c1bd63eb90c534e6db78))


## v0.0.2 (2024-06-14)

### Chore

* chore: fix line ending in GH workflow ([`b74fbca`](https://github.com/Jc2k/aiojellyfin/commit/b74fbca2b905c8e74f82dfbed34799428749cb8c))

* chore: ignore CHANGELOG spellings ([`1a2d722`](https://github.com/Jc2k/aiojellyfin/commit/1a2d72255188f59dc8220ae375fcdab66e902aa3))

### Fix

* fix: rework gh release pipeline ([`6e7d776`](https://github.com/Jc2k/aiojellyfin/commit/6e7d7768d6c851f5362175156485435dce8cdc8e))

* fix: remove environment from ci definition ([`0d12961`](https://github.com/Jc2k/aiojellyfin/commit/0d129613ff657dd3d7db17e77d22b8393354e2e2))


## v0.0.1 (2024-06-14)

### Chore

* chore: don&#39;t publish to pypi direct from main ([`58c77e6`](https://github.com/Jc2k/aiojellyfin/commit/58c77e66fd4d29a8e5a82faf715ae6d7ebe2e347))

* chore: add gh release workflow ([`00cd418`](https://github.com/Jc2k/aiojellyfin/commit/00cd4189937a10cbd9a48c8a421594f5144e1ade))

* chore: fix typos ([`dd20522`](https://github.com/Jc2k/aiojellyfin/commit/dd20522432672de9337f57c89b92f384325c2632))

* chore: enable mypy checking ([`40a516f`](https://github.com/Jc2k/aiojellyfin/commit/40a516ffaecb32e63d311b613b0d8234cf0daa16))

### Fix

* fix: update query terms to match the Jellyfin schema ([`bffcfa4`](https://github.com/Jc2k/aiojellyfin/commit/bffcfa450ea13c9d6c6923d7a04421f3872f3832))


## v0.0.0 (2024-06-14)

### Chore

* chore: update the GH action for PyPI publishing ([`ae3510a`](https://github.com/Jc2k/aiojellyfin/commit/ae3510ad484efde9d56fad9a432673701c490e00))

* chore: bring module up to latest ruff standards ([`f80e01c`](https://github.com/Jc2k/aiojellyfin/commit/f80e01c335cd1d45e1d95d80587b93f04b470d58))

* chore: add dependencies for ci lint tooling ([`9de64bf`](https://github.com/Jc2k/aiojellyfin/commit/9de64bfa39778db763c2cf6bb2e3f959f0778b9b))

* chore: Remove unused dependency fro GH action config ([`9e05e4f`](https://github.com/Jc2k/aiojellyfin/commit/9e05e4f6246a6614e68f52569bacdc982d198fb7))

* chore: Run pre-commit on CI ([`e43879f`](https://github.com/Jc2k/aiojellyfin/commit/e43879fac1f0532f6eb8267e4208b8e74c5cc835))

* chore: Add scaffolding for pre-commit on CI ([`6508cc8`](https://github.com/Jc2k/aiojellyfin/commit/6508cc894078c148611d4d76c4139db4f06b21a4))

* chore: Add github release workflow ([`6144df8`](https://github.com/Jc2k/aiojellyfin/commit/6144df89ac4c6c90a7c8e5298372def9645441a7))

### Unknown

* Allow using an injected ClientSession ([`0b73406`](https://github.com/Jc2k/aiojellyfin/commit/0b73406370dfda7e99b237a53adab067c07c46c8))

* Testing fixes ([`2a6d0c3`](https://github.com/Jc2k/aiojellyfin/commit/2a6d0c3d5132df7c35900fcc5524dd5b982de02b))

* Cleanup and add SessionConfiguration ([`4e00d55`](https://github.com/Jc2k/aiojellyfin/commit/4e00d5589f6209238cec66ea9dda511e0797ba20))

* Implement search_media_items ([`c1e7a41`](https://github.com/Jc2k/aiojellyfin/commit/c1e7a41cd6f4251e3cf327bf0663dffe8b58daee))

* Implement get_item ([`e500ede`](https://github.com/Jc2k/aiojellyfin/commit/e500ede1168650939e6a76c598f8ccdbbacf97b6))

* Implement client.artwork ([`441f0d8`](https://github.com/Jc2k/aiojellyfin/commit/441f0d8f2f6402d8684b247fd7e2372f052a771e))

* ruff check ([`2f52eef`](https://github.com/Jc2k/aiojellyfin/commit/2f52eef6e94a2ee56c4bcb3d15efd25dbd9f94a6))

* format ([`d57b763`](https://github.com/Jc2k/aiojellyfin/commit/d57b763717e581d9f5488a8eebf64b59eac9701c))

* Sigh ([`d352f00`](https://github.com/Jc2k/aiojellyfin/commit/d352f00218904c0a5f5ed52c15d27442c00ea023))

* Initial commit ([`1affba3`](https://github.com/Jc2k/aiojellyfin/commit/1affba374afada28b6848ddc9f17fb82bf625a0b))
