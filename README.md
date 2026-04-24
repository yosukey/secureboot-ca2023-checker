# Secure Boot UEFI CA 2023 Checker

Windows の Secure Boot データベース (db) に **Windows UEFI CA 2023** 証明書が登録されているかを確認する GUI ツールです。

この証明書は、2026 年以降の Windows Update 配信において起動可能なブートローダーの署名検証に使用される予定であり、登録されていない場合は将来の更新適用後に起動不能になるリスクがあります。

---

## ダウンロードと実行方法

1. [Releases](../../releases) ページを開く
2. 最新リリースの `SecureBootCA2023Checker-vX.Y.Z.exe` をダウンロード
3. ダウンロードしたファイルをダブルクリックして起動
4. 「チェック開始」ボタンを押す

> **必要環境:** Windows 10 / 11（PowerShell 5.1 以上）、インストール不要

---

## 実行結果の見方

| 表示 | 意味 |
|---|---|
| ✔ Windows UEFI CA 2023 が登録されています | 証明書が Secure Boot データベースに存在する。対応済み |
| ✘ Windows UEFI CA 2023 が登録されていません | 証明書が未登録。Windows Update を適用するか、BIOS/UEFI の Secure Boot データベースをリセットして対応が必要 |

---

## SmartScreen 警告について

このツールは個人が作成した署名なし実行ファイルであるため、初回起動時に Windows Defender SmartScreen の警告が表示されることがあります。これはコード署名証明書が購入・取得されていないことによるもので、ツール自体に問題があるわけではありません。

**警告を回避して実行する手順:**

1. 「Windows によって PC が保護されました」ダイアログが表示されたら
2. 「詳細情報」をクリック
3. 「実行」ボタンが現れるのでクリック

または、ファイルを右クリック →「プロパティ」→「セキュリティ」欄の「許可する」にチェックを入れて「OK」でも解除できます。

心配な場合はソースコード (`checker.py`) を直接確認し、Python 環境で実行してください。

```bash
pip install pyinstaller  # ビルドする場合のみ
python checker.py
```
