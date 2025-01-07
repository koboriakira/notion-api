# Changelog

## [2.8.2](https://github.com/koboriakira/notion-api/compare/v2.8.1...v2.8.2) (2025-01-07)


### Bug Fixes

* BuyStatusからのステータスタイプの変換ロジックを修正 ([4e6365a](https://github.com/koboriakira/notion-api/commit/4e6365af4b9c02143e996f82cd5f5ffc8d28a78e))

## [2.8.1](https://github.com/koboriakira/notion-api/compare/v2.8.0...v2.8.1) (2025-01-07)


### Bug Fixes

* スケジュールタスクの自動実行機能の不具合を修正 ([#81](https://github.com/koboriakira/notion-api/issues/81)) ([8b261cf](https://github.com/koboriakira/notion-api/commit/8b261cfab1a020ee4d47df933fb857c5077f2e2f))
* ルーチンタスク作成時にタスクを保存するロジックを修正 ([6e3321a](https://github.com/koboriakira/notion-api/commit/6e3321a2cbed64f030a8d5766dade037e3e39b28))

## [2.8.0](https://github.com/koboriakira/notion-api/compare/v2.7.0...v2.8.0) (2025-01-06)


### Features

* Implement BookOpenbdApi for fetching book details by ISBN ([#79](https://github.com/koboriakira/notion-api/issues/79)) ([cadd362](https://github.com/koboriakira/notion-api/commit/cadd362c6e65264c5920fb8ae531dddfa05cc97d))


### Bug Fixes

* Update task creation logic in InboxService to use Task model ([19141d6](https://github.com/koboriakira/notion-api/commit/19141d663bb677b1b135b2d46cb83308f3318edd))
* Update TaskContextType comparison to use value instead of name ([b333fbf](https://github.com/koboriakira/notion-api/commit/b333fbf5bdf9339c8e3545fb3697534990c9233a))

## [2.7.0](https://github.com/koboriakira/notion-api/compare/v2.6.2...v2.7.0) (2025-01-01)


### Features

* Add end-to-end tests for gif/jpeg page creation and update image handling ([e03dc46](https://github.com/koboriakira/notion-api/commit/e03dc4618dcaf38a59345175d54e0510c16801dd))

## [2.6.2](https://github.com/koboriakira/notion-api/compare/v2.6.1...v2.6.2) (2025-01-01)


### Bug Fixes

* Update block_id reference in ShareImageUsecase for correct daily log entry ([ad8332c](https://github.com/koboriakira/notion-api/commit/ad8332c5a2e89d206c6df3ba7143baa0dce70585))

## [2.6.1](https://github.com/koboriakira/notion-api/compare/v2.6.0...v2.6.1) (2025-01-01)


### Bug Fixes

* スケジュール開始の機能を修正 ([59b9e1a](https://github.com/koboriakira/notion-api/commit/59b9e1ae601e7c54e1904bb7f02274ab2a892ecc))

## [2.6.0](https://github.com/koboriakira/notion-api/compare/v2.5.3...v2.6.0) (2024-12-31)


### Features

* Add TaskContext class as MultiSelect for task categorization ([8cc3737](https://github.com/koboriakira/notion-api/commit/8cc3737f91d6174730c1841c2bc1e2e64095cd5d))

## [2.5.3](https://github.com/koboriakira/notion-api/compare/v2.5.2...v2.5.3) (2024-12-29)


### Bug Fixes

* Simplify datetime conversion logic in _convert_datetime function ([966638d](https://github.com/koboriakira/notion-api/commit/966638d4da401e68af7e0c7efeeda09a7d9282fc))

## [2.5.2](https://github.com/koboriakira/notion-api/compare/v2.5.1...v2.5.2) (2024-12-28)


### Bug Fixes

* Rename date conversion functions for clarity and improve type handling ([a9e35a9](https://github.com/koboriakira/notion-api/commit/a9e35a9719dfab80648b9171b7a68aa3eeb82c63))

## [2.5.1](https://github.com/koboriakira/notion-api/compare/v2.5.0...v2.5.1) (2024-12-28)


### Bug Fixes

* Remove unnecessary days parameter from complete task function ([bf7d9ce](https://github.com/koboriakira/notion-api/commit/bf7d9ce44c0977513ac83359de41dc5ce5afcb66))

## [2.5.0](https://github.com/koboriakira/notion-api/compare/v2.4.0...v2.5.0) (2024-12-28)


### Features

* Add complete task functionality to webhook handling ([71e43d5](https://github.com/koboriakira/notion-api/commit/71e43d524d16126f4deee7fc289288388ff60cba))
* Add postpone task functionality and refactor webhook handling ([708d1ca](https://github.com/koboriakira/notion-api/commit/708d1ca78105715fe9da4f723cfdaf77e2a16245))


### Bug Fixes

* 削除したメソッドを利用しない ([d717504](https://github.com/koboriakira/notion-api/commit/d717504d24b375256ad5a200512e530e8401aad6))
* 削除漏れを対応 ([5567093](https://github.com/koboriakira/notion-api/commit/55670932235e52bb6dbd0cdc36030077fe1893c2))

## [2.4.0](https://github.com/koboriakira/notion-api/compare/v2.3.0...v2.4.0) (2024-12-27)


### Features

* Lotionのバージョンアップに合わせる ([#67](https://github.com/koboriakira/notion-api/issues/67)) ([f2574c3](https://github.com/koboriakira/notion-api/commit/f2574c3368e814717eae96ad1bbaca5dca1f382d))

## [2.3.0](https://github.com/koboriakira/notion-api/compare/v2.2.0...v2.3.0) (2024-12-26)


### Features

* PJ化のボタンを作成 ([#59](https://github.com/koboriakira/notion-api/issues/59)) ([43adba8](https://github.com/koboriakira/notion-api/commit/43adba825a60f5129e76b3ee7990cce06698264c))
* スケジュールの自動開始に対応 ([4220e74](https://github.com/koboriakira/notion-api/commit/4220e74c33469b8e1d5b77e72f9db38a0d928679))
* 開始ボタンのWebhook化 ([#61](https://github.com/koboriakira/notion-api/issues/61)) ([310d8fb](https://github.com/koboriakira/notion-api/commit/310d8fb24a065fc46d622f59d3d6421c3131e705))


### Bug Fixes

* Titleプロパティの扱いを改善 ([#56](https://github.com/koboriakira/notion-api/issues/56)) ([0f7de18](https://github.com/koboriakira/notion-api/commit/0f7de18fe9c08847962ae48f6660051d6f178c94))

## [2.2.0](https://github.com/koboriakira/notion-api/compare/v2.1.0...v2.2.0) (2024-12-25)


### Features

* 「あとで」をしたときに完了時刻を記録する ([f030490](https://github.com/koboriakira/notion-api/commit/f0304906a89360a9f95ef3dde2b1da160b85591a))
* GitHubの情報を取得する ([#54](https://github.com/koboriakira/notion-api/issues/54)) ([db02d14](https://github.com/koboriakira/notion-api/commit/db02d149b8213e2f408c48a8251320e0c747806d))
* あとまわしにしたタスク情報をきちんとコピーする ([#53](https://github.com/koboriakira/notion-api/issues/53)) ([9375a95](https://github.com/koboriakira/notion-api/commit/9375a951326ff35e98db59bb5c9cb2221cdb5aa8))
* 完了タスクの先頭にチェックマークを付与する ([#36](https://github.com/koboriakira/notion-api/issues/36)) ([c268e13](https://github.com/koboriakira/notion-api/commit/c268e13d32108928b0bc9e7d53c1c5f7cf406269))


### Bug Fixes

* Gmailの送信元アドレスの処理パターンを追加 ([b537f3b](https://github.com/koboriakira/notion-api/commit/b537f3b24fe9446ae869a14b3c90162399d6e690))
* 経過時間の表示を正す ([b60019c](https://github.com/koboriakira/notion-api/commit/b60019c8925f0e44129a70265399261875a60b05))

## [2.1.0](https://github.com/koboriakira/notion-api/compare/v2.0.0...v2.1.0) (2024-12-24)


### Features

* ai_advice機能のタスク取得ロジックを改善し、進行中タスクの通知を追加 ([4e48d57](https://github.com/koboriakira/notion-api/commit/4e48d5763c2daec9ede2ad62233c3ad04a4549d8))
* AIアドバイス機能を実装 ([#42](https://github.com/koboriakira/notion-api/issues/42)) ([bd7562c](https://github.com/koboriakira/notion-api/commit/bd7562cc2703d707bd41295feba96c84f2201cae))
* LINE通知機能を追加 ([#48](https://github.com/koboriakira/notion-api/issues/48)) ([49e77aa](https://github.com/koboriakira/notion-api/commit/49e77aab41facd7f041e98f37efa60eb6adeb493))
* NotionからのWebhookを受け付けるAPIを作成 ([2ff0233](https://github.com/koboriakira/notion-api/commit/2ff0233515f5b6a4eeee7f8f5c6d652c7f7fe2da))
* NotionのWebhookを受け取るAPIを作成 ([#44](https://github.com/koboriakira/notion-api/issues/44)) ([68a863f](https://github.com/koboriakira/notion-api/commit/68a863fba27782c89b5e4580ae7ac7d4c023ae2a))
* プロジェクト関連タスクのタスク種別変更機能を無効化 ([fd7a1fa](https://github.com/koboriakira/notion-api/commit/fd7a1fae7bacacca2b7e9cab5c6e6f7df4dc217c))
* 時間ごとに現状を知らせるバッチを作成 ([#49](https://github.com/koboriakira/notion-api/issues/49)) ([86cb94e](https://github.com/koboriakira/notion-api/commit/86cb94e1dba41a61209e0e73553849c19e809ed7))
* 目標のレビューも含める ([#37](https://github.com/koboriakira/notion-api/issues/37)) ([ea84fbe](https://github.com/koboriakira/notion-api/commit/ea84fbe74ffa7ae1a5dc711c64eaf86bfc707628))
* 目標ページに進行中プロジェクトのメンションを載せる ([#33](https://github.com/koboriakira/notion-api/issues/33)) ([74a1985](https://github.com/koboriakira/notion-api/commit/74a198505d63fb7ea6e193be388a63639b5e3751))
* 見出しに日付を加える ([5d9f0a3](https://github.com/koboriakira/notion-api/commit/5d9f0a331e8a1bb48fd071ba5c800cc366b60019))


### Bug Fixes

* 「アクションプラン」ではなく「今週の目標」に変更 ([02240ae](https://github.com/koboriakira/notion-api/commit/02240aea254d23047370b43e8788534fdc858730))
* import整理の忘れを対応 ([6b5ad12](https://github.com/koboriakira/notion-api/commit/6b5ad123ea52f0cce087ba7669f63a9e73b96a9a))
* PageIdをimportしない ([#46](https://github.com/koboriakira/notion-api/issues/46)) ([d4f6642](https://github.com/koboriakira/notion-api/commit/d4f66422efd4e232d4225978c83628f8dd08cf11))
* PageIdを利用しない ([#45](https://github.com/koboriakira/notion-api/issues/45)) ([2be46ea](https://github.com/koboriakira/notion-api/commit/2be46ea3fae719e49ce1aa1a29fe440c45928a62))
* ただしい条件をつくる ([bc51625](https://github.com/koboriakira/notion-api/commit/bc51625168e8deed6c5b219010d1e1639c38c9af))

## [2.0.0](https://github.com/koboriakira/notion-api/compare/v1.9.0...v2.0.0) (2024-12-16)


### ⚠ BREAKING CHANGES

* lotionを利用する ([#27](https://github.com/koboriakira/notion-api/issues/27))

### Miscellaneous Chores

* lotionを利用する ([#27](https://github.com/koboriakira/notion-api/issues/27)) ([460b8e2](https://github.com/koboriakira/notion-api/commit/460b8e2b876d1c1634ce6580808df577d496aa3a))

## [1.9.0](https://github.com/koboriakira/notion-api/compare/v1.8.0...v1.9.0) (2024-12-14)


### Features

* Add routine task creation and external calendar synchronization endpoints ([46312ef](https://github.com/koboriakira/notion-api/commit/46312ef65dc2c9c6f39bcbaff6737658e27cbdb4))
* Update DAILY_LOG ID and add batch router with create_next_schedule endpoint ([96626a0](https://github.com/koboriakira/notion-api/commit/96626a04c92dab8ecbd07e04666adefb19d909b5))
* スケジュールタスク作成のときに重複が起きないようにする ([b744acb](https://github.com/koboriakira/notion-api/commit/b744acb650ae00df69b4d2787cf9a030b3f9b5a3))

## [1.8.0](https://github.com/koboriakira/notion-api/compare/v1.7.0...v1.8.0) (2024-12-08)


### Features

* ページに画像を追加するAPIを追加 ([#25](https://github.com/koboriakira/notion-api/issues/25)) ([c9e90a6](https://github.com/koboriakira/notion-api/commit/c9e90a6153a9d8ebc35389fdd96236b94078d45b))
* 飲食ページ作成機能を追加 ([#23](https://github.com/koboriakira/notion-api/issues/23)) ([b802579](https://github.com/koboriakira/notion-api/commit/b802579a4d3753e4fd026883a6b0873d2f37e074))

## [1.7.0](https://github.com/koboriakira/notion-api/compare/v1.6.1...v1.7.0) (2024-12-08)


### Features

* Notionからの複製リクエストに対応 ([#20](https://github.com/koboriakira/notion-api/issues/20)) ([0a78b6a](https://github.com/koboriakira/notion-api/commit/0a78b6a59014ee04797b105732ed91f6f1e0bf80))
* 今日見た動画を収集する機能を追加し、YouTube埋め込みURLを生成 ([a59305c](https://github.com/koboriakira/notion-api/commit/a59305c36e4bc3c6892f7efa889951c9ea5f316d))
* 動画リポジトリに挿入日時範囲で検索する機能を追加 ([e834bb4](https://github.com/koboriakira/notion-api/commit/e834bb4d5e708ac46280d0ab20fcda525e99eca7))
* 外部カレンダーを同期する新しい機能を追加し、毎日20時に実行されるようにスケジュールを設定 ([f8afd03](https://github.com/koboriakira/notion-api/commit/f8afd034e527f937d1daea54a9b6a495ad940aa4))
* 毎日実行されるタスクの延期機能を削除し、関連コードを整理 ([dd59693](https://github.com/koboriakira/notion-api/commit/dd596930727b718a62ce7931b510a5e874ec36fa))
* 画像のタイトルにuuidを指定し、URL欄も埋める ([17ea1ce](https://github.com/koboriakira/notion-api/commit/17ea1ce8560f4be89271a4fde1e41f38f8f758dd))
* 目標データベースのバックアップ機能を追加 ([e7519ab](https://github.com/koboriakira/notion-api/commit/e7519ab8ae0b2ced4173ce367400fb8d47385bd4))
* 週次レビューの各タスクに開始時刻を付与しない ([90241d5](https://github.com/koboriakira/notion-api/commit/90241d529a88f3e1e8b53dca379472d1b4c9dc49))


### Bug Fixes

* 12月の翌月が翌年の1月になるように修正 ([#19](https://github.com/koboriakira/notion-api/issues/19)) ([272f10b](https://github.com/koboriakira/notion-api/commit/272f10b0106e71b47a78c3fbbcdd433e3eac0eaa))
* Remove UUID from external image title generation in ExternalImageService ([2412358](https://github.com/koboriakira/notion-api/commit/24123586e5869f5924b30e6c2aec6ab43f008b90))
* VideoRepositoryImplをInjectorに追加し、CollectUpdatedPagesUsecaseに統合 ([f8f300a](https://github.com/koboriakira/notion-api/commit/f8f300a9d2b09528d8ce1317b837bfe6135f17b1))

## [1.6.1](https://github.com/koboriakira/notion-api/compare/v1.6.0...v1.6.1) (2024-11-22)


### Bug Fixes

* DynamoDBを利用する ([f71fac5](https://github.com/koboriakira/notion-api/commit/f71fac57ab01957661828e13ceb72efe97b4329f))
* remove unnecessary parameter from image processing function ([96b1195](https://github.com/koboriakira/notion-api/commit/96b1195483e014e3a0deefdb272a50826c820e41))
* コンストラクタの指定漏れを修正 ([e6effe6](https://github.com/koboriakira/notion-api/commit/e6effe6755969f5ecbd98a68efebd785b719addd))

## [1.6.0](https://github.com/koboriakira/notion-api/compare/v1.5.0...v1.6.0) (2024-11-19)


### Features

* 「_あとでチェック」フラグ機能を追加し、タスクの「あとまわし」処理を追加 ([6effd8a](https://github.com/koboriakira/notion-api/commit/6effd8abf345011702b80d1113a636e293c54d20))
* 「明日やる」ときは、開始時刻を消して翌日の日付のみ記載する ([35949e8](https://github.com/koboriakira/notion-api/commit/35949e84f0258823d5176628bdf31d1b64ac9b3f))
* Trashステータスのプロジェクトを削除する処理を実装 ([04d899b](https://github.com/koboriakira/notion-api/commit/04d899b195c1d8ef3719cd8c949f76b13907f21d))
* プロジェクトをバックアップ用にアーカイブする機能を追加 ([c3f26e7](https://github.com/koboriakira/notion-api/commit/c3f26e781eb4855d2f3dfd76116f6e2bbfeb92fd))

## [1.5.0](https://github.com/koboriakira/notion-api/compare/v1.4.0...v1.5.0) (2024-11-19)


### Features

* タスクの開始チェック機能を追加し ([6514655](https://github.com/koboriakira/notion-api/commit/65146556def6ffab9d76e98a71a1af90e54e97ca))
* 完了チェック機能を追加し、タスクの終了日時を更新するメソッドを実装 ([84a56ef](https://github.com/koboriakira/notion-api/commit/84a56ef93154ecb7433711c334148a662481e37f))
* 画像の取得機能を追加し、日付範囲に基づいて画像を処理するメソッドを実装 ([61b2b20](https://github.com/koboriakira/notion-api/commit/61b2b20077cef506acb77c89a079a3680fdeac0b))

## [1.4.0](https://github.com/koboriakira/notion-api/compare/v1.3.0...v1.4.0) (2024-11-17)


### Features

* 26時までの実行は前日分とする ([bfb925e](https://github.com/koboriakira/notion-api/commit/bfb925ed44be13a69f6804f0759cc52633c52f97))
* 重複したスケジュールタスクを作成しないようにする ([254cc6a](https://github.com/koboriakira/notion-api/commit/254cc6ae4f10c9e1a291dc3a8bef3cd72415375a))


### Bug Fixes

* improve date range checks in is_between method and filter tasks in move_tasks_to_backup_usecase ([6b28504](https://github.com/koboriakira/notion-api/commit/6b285044cad72fb6403e2b81d3b5570629196c5c))

## [1.3.0](https://github.com/koboriakira/notion-api/compare/v1.2.0...v1.3.0) (2024-11-16)


### Features

* 画像共有機能を追加 ([#12](https://github.com/koboriakira/notion-api/issues/12)) ([7176e25](https://github.com/koboriakira/notion-api/commit/7176e250127963a093b21445ed463f036395ca3f))

## [1.2.0](https://github.com/koboriakira/notion-api/compare/v1.1.0...v1.2.0) (2024-11-16)


### Features

* 自動ページ収集機能を削除 ([#10](https://github.com/koboriakira/notion-api/issues/10)) ([695d6b0](https://github.com/koboriakira/notion-api/commit/695d6b02f5f1fc76734616fc04de45f773f75284))

## [1.1.0](https://github.com/koboriakira/notion-api/compare/v1.0.0...v1.1.0) (2024-11-16)


### Miscellaneous Chores

* release 1.1.0 ([6840d75](https://github.com/koboriakira/notion-api/commit/6840d75bfe239df4af4df7d049b66446f35284a1))

## 1.0.0 (2024-11-15)


### Features

* 「明日やる」フラグの検索を追加 ([95ba5b3](https://github.com/koboriakira/notion-api/commit/95ba5b3ac3dfb1b4d54ed92473134f906a9772bc))
* 0時0分の場合は時刻を含んでいないとみなす ([efa75a5](https://github.com/koboriakira/notion-api/commit/efa75a5127d7ea6e193bcca529c2d64fa3b7bc82))
* Add "2分で終わる" task kind to KIND_LIST ([272131c](https://github.com/koboriakira/notion-api/commit/272131c6eb73bfb843990e8c9948f4c628b5fe3d))
* Add "外出" routine kind ([ed73163](https://github.com/koboriakira/notion-api/commit/ed731631519b3b557725fa9070a5feab8e0d0d34))
* Add "月末" routine kind ([d5afa7a](https://github.com/koboriakira/notion-api/commit/d5afa7a892b63a81bf3fc3a84f125101260ab626))
* Add "月末" routine kind with selected_id "6e0a84e9-17d8-49ec-8d75-117935f3c4ee" and selected_color "gray" ([ed57ca0](https://github.com/koboriakira/notion-api/commit/ed57ca0e9f69aa04eb2c73102543b1da801a7790))
* Add AppendFeelingUsecase and UpdateStatusUsecase ([86e9a27](https://github.com/koboriakira/notion-api/commit/86e9a2761b228452b02d1829d27875dab28bbd94))
* Add BATCH_TIMEOUT constant for lambda function creation ([9e87f04](https://github.com/koboriakira/notion-api/commit/9e87f04849616f25acd49fef9b05ccac1e991cbd))
* Add CI workflow for Gauge ([a0efe38](https://github.com/koboriakira/notion-api/commit/a0efe386d0d336b5ed41edee283ec0582fc8b268))
* Add complete_task endpoint to task router ([94c874c](https://github.com/koboriakira/notion-api/commit/94c874ce809562ab9dadf17fa1def005e5231ab1))
* Add create_routine_task method to TaskFactory ([41c6b3f](https://github.com/koboriakira/notion-api/commit/41c6b3f444bbe1d3562e7615d176eb2a24c992cb))
* Add dead letter queue support to NotionApi ([494c0ba](https://github.com/koboriakira/notion-api/commit/494c0ba45fb317f2e4294052bedf04596d1d9bb6))
* Add due_time method to RoutineTask ([2fa1096](https://github.com/koboriakira/notion-api/commit/2fa10966be3642e7b0e2d3866c151a5c98402893))
* Add e2e tests for task creation and deletion ([3ba6a28](https://github.com/koboriakira/notion-api/commit/3ba6a2854b4fc137a0a1280f816c27fadeabfa40))
* Add endpoint to get latest in-progress task ([3013e19](https://github.com/koboriakira/notion-api/commit/3013e19db7dd2e3e47c3698dd0b2d789c6bccb1c))
* Add error handling for NotFoundApiError in AddBookUsecase ([a7c7d84](https://github.com/koboriakira/notion-api/commit/a7c7d8407ab9966fec4bf492e011793c2e7d599b))
* Add from_str method to Artist class ([67e5cf3](https://github.com/koboriakira/notion-api/commit/67e5cf36a31c48587143597f27bc49f48ff6bf3e))
* Add Gauge e2e tests for task creation and deletion ([68be504](https://github.com/koboriakira/notion-api/commit/68be504ee695bc60082ccd8354aefac642a66492))
* Add Gauge e2e tests for task creation and deletion ([1e61fba](https://github.com/koboriakira/notion-api/commit/1e61fba2da9ee252d7a32ca2a3a0c58118d6c687))
* Add get_user_tweets method to LambdaTwitterApi class ([5a04294](https://github.com/koboriakira/notion-api/commit/5a04294c84c66fa591fcc10fa18093eecaa45149))
* Add ImportantFlag class for task domain ([a7e661b](https://github.com/koboriakira/notion-api/commit/a7e661b861023a5da6d7ff1c4ab629a33cb0232c))
* Add kind prefix to inbox task titles ([6a9f9b0](https://github.com/koboriakira/notion-api/commit/6a9f9b0d9715cf30a683ae521671ddb33de2a5a1))
* Add lazy loading for images in CollectUpdatedPagesUsecase ([73fcfc5](https://github.com/koboriakira/notion-api/commit/73fcfc5c16bbaba64f3f25a4f926f9df603e31b0))
* Add lazy loading for images in CollectUpdatedPagesUsecase ([b1c6466](https://github.com/koboriakira/notion-api/commit/b1c6466707c5343be845d655033d931ca4a148a3))
* Add lazy loading for images in CollectUpdatedPagesUsecase ([0ccfbfb](https://github.com/koboriakira/notion-api/commit/0ccfbfb3da9cc9185d7dd9fa491d607b40700945))
* Add lazy loading for images in page load ([9be1a19](https://github.com/koboriakira/notion-api/commit/9be1a19aef9faff26f80df783a19ecd60fe7bf39))
* Add lazy loading for restaurant cover image in RestaurantCreator ([3842fed](https://github.com/koboriakira/notion-api/commit/3842fed2616e97a9465c5ef929701577e0310968))
* Add lazy loading for restaurant cover image in RestaurantCreator ([fd5dff6](https://github.com/koboriakira/notion-api/commit/fd5dff67a89e18bbc4c08e4c6045fc148bd9ba5e))
* Add metrics and logs for error monitoring ([eb66919](https://github.com/koboriakira/notion-api/commit/eb66919946131cf3aa65756a603c50578c872c37))
* Add pomodoro_start_datetime property to Task model and update related classes ([2a4d4d4](https://github.com/koboriakira/notion-api/commit/2a4d4d4207b5fbf17caae863eb3932ea160879ad))
* Add ResetShoppingListUseCase ([df11df9](https://github.com/koboriakira/notion-api/commit/df11df94e2129d7b799d5bbfd7c6f0a0e2267933))
* Add routine task kind to TaskKind class ([de82d56](https://github.com/koboriakira/notion-api/commit/de82d5609ca460bddef8dc259f316f3d62a2b376))
* Add RoutineOption class for task domain ([a9ba41d](https://github.com/koboriakira/notion-api/commit/a9ba41d52e932cff15128b8ec3312ac53376288d))
* Add RoutineToDoTask class for task domain ([3efd3b9](https://github.com/koboriakira/notion-api/commit/3efd3b91d754b779a015b7cb61f2d44125d8e8c3))
* Add Slack notifications for daily log updates ([f818fdb](https://github.com/koboriakira/notion-api/commit/f818fdbcfb0303ab2237ef425d3b973dc5b849f4))
* Add start_task endpoint to task router ([0fb1fcc](https://github.com/koboriakira/notion-api/commit/0fb1fcc414719fdbfdc9c621f3996446fd213a04))
* Add support for completing tasks in e2e tests ([8d2aaf9](https://github.com/koboriakira/notion-api/commit/8d2aaf9e424f0ebe3158fe3f392a0a059063ee47))
* Add support for embedding bookmarks in inbox task pages ([fafe3a0](https://github.com/koboriakira/notion-api/commit/fafe3a01fb0b9c73a1f253ac79a7857981040ec3))
* Add support for gauge-current tag in e2e tests ([ede6855](https://github.com/koboriakira/notion-api/commit/ede68554d22247547bd9ac262af92c6d51817060))
* Add support for Japanese date in account book creation ([a571815](https://github.com/koboriakira/notion-api/commit/a5718153079dc979965c17368ec9b7081b581bd8))
* Add support for Restaurant and Book page types in InboxService ([f786079](https://github.com/koboriakira/notion-api/commit/f786079e4a8534a36f706494c26b9e90a4ff3a5f))
* Add support for Webclip page type in InboxService ([7b6c4c7](https://github.com/koboriakira/notion-api/commit/7b6c4c7e0346034ce4e9bbcefd52d83a934a406c))
* Add TaskContextType property to ToDoTask ([e16cadd](https://github.com/koboriakira/notion-api/commit/e16cadd029360b2dff7a069bc343665bbb53e940))
* Add Twitter user tweets to daily log ([6c29131](https://github.com/koboriakira/notion-api/commit/6c291318943a3c7229f6b141c66e153bbb8e3566))
* Add upload_as_file method to SlackClient ([08118de](https://github.com/koboriakira/notion-api/commit/08118dea50786ef6b74b1fa7b8f545bffb9f15a2))
* Add vscode-pylance extension and enable basic type checking in Python analysis ([0465455](https://github.com/koboriakira/notion-api/commit/046545593dd72ed5c9e50826b486b06b7dc9be9f))
* Create and delete tasks with Japanese names ([3b56ace](https://github.com/koboriakira/notion-api/commit/3b56acead6a21c829d9d3a10b4c774d2834cfda5))
* Fix channel type assignment in CollectUpdatedPagesUsecase ([24cfb9a](https://github.com/koboriakira/notion-api/commit/24cfb9ac4ef079c8a575af706cd20b76d8db866b))
* Fix error handling in ErrorReporter ([76948f8](https://github.com/koboriakira/notion-api/commit/76948f82e54df732ec10db206d4f85c39b20fab7))
* Fix typo in ci_gauge.yml ([48636e7](https://github.com/koboriakira/notion-api/commit/48636e70127be24a3925ae86f706ac4461cfd36c))
* Handle TypeError in append_block_children method ([ce63f9e](https://github.com/koboriakira/notion-api/commit/ce63f9e439f88d77b6a5a33200b964429c1baa28))
* Implement search method in SongRepository ([7b84498](https://github.com/koboriakira/notion-api/commit/7b84498fd1d255e8d5f810422372061194eb59cb))
* Improve error reporting for public API unavailability in ErrorReporter ([0e2329a](https://github.com/koboriakira/notion-api/commit/0e2329a2a11123a8998c4da1c5307837cbf84e37))
* Refactor Embed class to improve code readability and maintainability ([117e38d](https://github.com/koboriakira/notion-api/commit/117e38dfce8a7db5946cf24120b60ea019047dda))
* Refactor FindLatestInprogressTaskUsecase to handle empty task list ([0a23384](https://github.com/koboriakira/notion-api/commit/0a233840ca4deca83dc486da152ff122a06e78fa))
* Refactor FindLatestInprogressTaskUsecase to handle empty task list ([4591130](https://github.com/koboriakira/notion-api/commit/4591130e9263d77992851495b79fbcac8c097182))
* Refactor Paragraph class initialization ([07e8ac2](https://github.com/koboriakira/notion-api/commit/07e8ac28364beab3285bbbd58d9ebbd08d42c0ac))
* Refactor TaskRepositoryImpl to use BasePage for type casting ([dfa47ae](https://github.com/koboriakira/notion-api/commit/dfa47aefcfaa02ed3a199b0c6a0c37abe90673b5))
* Refactor TaskRepositoryImpl to use BasePage for type casting ([f3e1bcc](https://github.com/koboriakira/notion-api/commit/f3e1bcc40975bb026557e474a7a2d890ed64e491))
* Refactor Title property class and improve error handling ([94ad3ef](https://github.com/koboriakira/notion-api/commit/94ad3efcd4d5d4129a8ed00bcc6c5c867145e49a))
* Remove AddWebclipUsecase and related code ([7a0ea11](https://github.com/koboriakira/notion-api/commit/7a0ea113080c0947f2d79b8c88fa7f160a371381))
* Reset shopping list buy status in every_minutes_batch.py ([94ef426](https://github.com/koboriakira/notion-api/commit/94ef426618b9509922e58c3da4dace41d28e3bf8))
* Update account book page title ([a116e05](https://github.com/koboriakira/notion-api/commit/a116e05ca16ff9a94492ad23f50e38ac5f0bde54))
* Update CollectUpdatedPagesUsecase to use embed_tweet_html ([1329df9](https://github.com/koboriakira/notion-api/commit/1329df9070b33c70472a57c168bce3761b27f276))
* Update CollectUpdatedPagesUsecase to use embed_tweet_html ([519d928](https://github.com/koboriakira/notion-api/commit/519d928cb6cf792584eabf61d64357c35038b65a))
* Update complete_task endpoint URL in task router ([7947d48](https://github.com/koboriakira/notion-api/commit/7947d48a96923a3567345acfa1b87cabbe3dfd7e))
* Update CreateRoutineTaskUseCase to handle next action tasks ([de2bf7c](https://github.com/koboriakira/notion-api/commit/de2bf7ce24fadbfce5b11d1d7c9464dfb38676ff))
* Update CreateRoutineTaskUseCase to use ROUTINE task kind type ([7e7bf6c](https://github.com/koboriakira/notion-api/commit/7e7bf6c63bd4f48a3cadf83d6489998d9997e625))
* Update CreateRoutineTaskUseCase to use ROUTINE task kind type ([a8578e3](https://github.com/koboriakira/notion-api/commit/a8578e315eab08ed88eb2e8378fe73a33fdc82a0))
* Update Lambda Layer generation to use Python 3.12 ([9a6f436](https://github.com/koboriakira/notion-api/commit/9a6f4362a30aa3761d120b5c7b907525b3579573))
* Update OpenAI model usage in code ([2f159e0](https://github.com/koboriakira/notion-api/commit/2f159e0965f9c0d33959d839eeffed1e5e7850ab))
* Update order calculation for task priority ([1c288b2](https://github.com/koboriakira/notion-api/commit/1c288b24ded75b6618b112f96836ad518bad1c2f))
* Update pyproject.toml with indentation settings ([4885218](https://github.com/koboriakira/notion-api/commit/48852186d46472c61efcf5d3f24e884f08a9d959))
* Update Python version to 3.12 and dependencies ([98c22af](https://github.com/koboriakira/notion-api/commit/98c22af606a4b0b9ac48b295e08bb7979e828617))
* Update scheduler config for more frequent execution ([0c76f40](https://github.com/koboriakira/notion-api/commit/0c76f403249326bd5d5bde087b05fd7d69743e8a))
* Update Slack notifications for daily log updates and add lazy loading for images in page load ([9bd14a6](https://github.com/koboriakira/notion-api/commit/9bd14a65986a3f664d32a1705e9666454ae22402))
* Update Song class to include Spotify track ID ([d7ae346](https://github.com/koboriakira/notion-api/commit/d7ae3467967fbe9c45bbe2666a2f0c0d0eb780b2))
* Update start_date to use date instead of datetime in TestTaskFactory ([547d5de](https://github.com/koboriakira/notion-api/commit/547d5de9809e42fde651a330b584479aac9f9a77))
* Update Task class to include Task type union ([9896a82](https://github.com/koboriakira/notion-api/commit/9896a82bdfca567445206de0215bfcd7cd1e98be))
* Update task status update method to use "DONE" instead of "COMPLETED" ([07b6f44](https://github.com/koboriakira/notion-api/commit/07b6f44d051ed54cb915ebc5a335c11304be99e8))
* Update task update methods to return updated task object ([68e2ee9](https://github.com/koboriakira/notion-api/commit/68e2ee90f4e1ba3306d531567c6fa4995fadbc43))
* Update Task.order calculation logic ([fb7f1ee](https://github.com/koboriakira/notion-api/commit/fb7f1eea84a12ba44fb02c500f0bc2577ac3a1a4))
* タイトルが空のページを削除するバッチ処理を追加 ([cb722c1](https://github.com/koboriakira/notion-api/commit/cb722c1bbdfc9343668b5ec96b85c3db29957cc9))
* チェックボックスの検索条件を追加 ([342dcf3](https://github.com/koboriakira/notion-api/commit/342dcf32fff76f0c3957af1bde95045a189cdf37))
* 明日へ延期する機能をバッチ処理に追加 ([bc2a9fa](https://github.com/koboriakira/notion-api/commit/bc2a9fa73d1696e4d4d54ee5e5f163c0b36a394c))
* 明日やるフラグのフィールドを追加 ([3d9372c](https://github.com/koboriakira/notion-api/commit/3d9372cbb6be01c8a9e694880d7a228a7791faa9))
* 明日やる場合の変更ユースケースを作成 ([7192a89](https://github.com/koboriakira/notion-api/commit/7192a89643c0cf5b9900d4a13306128a3b10e794))
* 検索を高速化する ([056c22d](https://github.com/koboriakira/notion-api/commit/056c22d4384401a0c8779e550320bc9bd3eec38b))
* 締め切りも1日伸ばす ([4ba66d8](https://github.com/koboriakira/notion-api/commit/4ba66d80f0f27215272b118ef17028f82de33cc4))


### Bug Fixes

* 不具合を修正 ([f961a05](https://github.com/koboriakira/notion-api/commit/f961a05348a0df5894e867925435db09ebd7adb6))
* 実施日を翌日に延期するバッチ処理を修正 ([6c9e14a](https://github.com/koboriakira/notion-api/commit/6c9e14ae03065584dff4ebbbb034062dad85822d))
