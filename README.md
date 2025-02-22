## プロンプト管理システム / Prompt Management System

### 概要 / Overview
**日本語**:  
このプロジェクトは、ユーザーがプロンプトとその結果を保存、読み込み、編集できる対話型のツールです。Groq APIを通じてLlama 3モデルから応答を取得する機能や、手動での結果入力に対応しています。Llama 3を採用した理由は、コストがかからない点にあり、無料でありながら高性能なモデルを活用して効率的なプロンプト管理を実現します。データはJSON形式で保存され、編集履歴も記録されるため、過去のやり取りを簡単に振り返ることができます。  

**English**:  
This project is an interactive tool that allows users to save, load, and edit prompts and their results. It supports retrieving responses from the Llama 3 model via the Groq API or manual result input. Llama 3 was chosen because it’s cost-free, enabling efficient prompt management with a high-performance model at no expense. Data is stored in JSON format with edit history, making it easy to review past interactions.

### 従来の不満 / Motivation
**日本語**:  
プロンプトエンジニアリングにおいて、プロンプトだけを管理するのでは十分ではありません。プロンプトとその出力結果、さらにPDFなどの添付資料をセットで管理する必要性を感じていました。このツールでは、そうした課題を解決し、一元的な管理を可能にすることを目指しています。  

**English**:  
In prompt engineering, managing prompts alone isn’t enough. I felt the need to manage prompts, their outputs, and attachments like PDFs as a set. This tool aims to address that challenge by enabling unified management.

### 機能 / Features
*   **プロンプトと結果の保存 / Saving Prompts and Results**:  
    *   Groq API経由でLlama 3モデルを使用するか、手動で結果を入力できます。/ Use the Llama 3 model via Groq API or input results manually.  
    *   モデル名や追加情報（トーン、キーワードなど）を指定できます。/ Specify model name, tone, keywords, etc.  
    *   データを`prompts`フォルダにJSONファイルとして保存します。/ Save data as JSON files in the `prompts` folder.  
*   **プロンプトの読み込み / Loading Prompts**:  
    *   保存済みのプロンプト、結果、追加情報、編集履歴を表示できます。/ Display saved prompts, results, additional info, and edit history.  
*   **プロンプトの編集 / Editing Prompts**:  
    *   既存のプロンプトや結果を編集し、再生成も可能です。/ Edit existing prompts or results and regenerate them.  
    *   編集履歴を保存します。/ Save edit history.  
*   **対話型メニュー / Interactive Menu**:  
    *   操作が簡単なメニュー形式のインターフェースです。/ An easy-to-use menu-based interface.

### 依存関係 / Dependencies
*   **Python 3.x**  
*   **`groq` パッケージ（Groq APIを使用するため） / `groq` package (for Groq API)**  
*   **`python-dotenv` パッケージ（オプション: 環境変数の読み込みに使用） / `python-dotenv` package (optional: for loading environment variables)**  

### セットアップ / Setup
1.  **リポジトリの取得 / Obtaining the Repository**:  
    *   **Gitを使用してクローン (推奨) / Clone with Git (Recommended)**:  
        Gitがインストールされている場合は、以下のコマンドを実行してリポジトリをローカルにクローンします。/ If Git is installed, run the following command to clone the repository locally:  
        ```bash
        git clone https://github.com/Taro-t-dog/prompt_save.git
        ```  
        ※ `<リポジトリのURL>`はGitHubなどの実際のURLに置き換えてください。/ Replace `<repository URL>` with the actual URL (e.g., `https://github.com/Taro-t-dog/prompt_save.git`).  
    *   **ZIPファイルとしてダウンロード / Download as ZIP**:  
        Gitを使用しない場合は、リポジトリのZIPファイルをダウンロードできます。/ If not using Git, download the repository as a ZIP file:  
        1. GitHubなどのリポジトリページを開きます。/ Open the repository page on GitHub.  
        2. 「Code」ボタンをクリックし、「Download ZIP」を選択します。/ Click the "Code" button and select "Download ZIP."  
        3. ダウンロードしたZIPファイルを解凍します。/ Unzip the downloaded file.  

2.  **必要なパッケージのインストール / Installing Required Packages**:  
    *   このプロジェクトでは、以下のPythonパッケージが必要です。/ This project requires the following Python packages:  
        *   `groq`  
        *   `python-dotenv` (オプション / optional: 環境変数の読み込みに使用 / for loading environment variables)  
    *   **プログラム実行時の自動インストール / Auto-installation on Execution**:  
        プログラムを実行すると、不足しているパッケージが自動的にインストールされる場合があります。/ Running the program may automatically install missing packages.  
    *   **手動インストールが必要な場合 / Manual Installation if Needed**:  
        プログラム実行中にエラーが出た場合は、以下のコマンドでインストールしてください。/ If an error occurs during execution, install manually with these commands:  
        ```bash
        pip install groq  # Groq APIクライアント / Groq API client
        pip install python-dotenv  # 環境変数管理 (オプション) / Environment variable management (optional)
        ```  
    *   **仮想環境の利用 (オプション) / Using a Virtual Environment (Optional)**:  
        Pythonプロジェクトでは、仮想環境を使用すると便利です。仮想環境を作成すると、プロジェクトに必要なパッケージをシステム全体とは別に管理できます。仮想環境の作成と有効化の手順は以下の通りです。ただし、この手順は必須ではありません。/ Using a virtual environment is convenient for Python projects, allowing you to manage project-specific packages separately. Here are the steps (optional):  
        - 仮想環境作成 / Create: `python -m venv venv`  
        - 有効化 / Activate:  
          - Windows: `venv\Scripts\activate`  
          - macOS/Linux: `source venv/bin/activate`  

3.  **Groq APIキーの設定 / Setting Up the Groq API Key**:  
    *   このプログラムを実行するには、Groq APIキーが必要です。/ This program requires a Groq API key.  
    *   Groqのアカウントを作成し、APIキーを取得してください。[https://console.groq.com/login](https://console.groq.com/login) / Create a Groq account and obtain an API key at [https://console.groq.com/login](https://console.groq.com/login).  
    *   **環境変数の設定 / Setting Environment Variables**:  
        取得したAPIキーを環境変数として設定します。設定方法はお使いのOSによって異なります。/ Set the obtained API key as an environment variable, depending on your OS:  
        *   **Windows**:  
            1. 検索バーに「環境変数」と入力し、「システム環境変数の編集」を選択します。/ Search for "environment variables" and select "Edit system environment variables."  
            2. 「環境変数」ボタンをクリックします。/ Click the "Environment Variables" button.  
            3. 「システム環境変数」または「ユーザー環境変数」に新しい変数を作成します。/ Create a new variable under "System" or "User" variables.  
            4. 変数名を`GROQ_API_KEY`、値をあなたのGroq APIキーに設定します。/ Set the name to `GROQ_API_KEY` and the value to your Groq API key.  
            5. OKをクリックして保存します。/ Click OK to save.  
        *   **macOS/Linux**:  
            1. ターミナルを開きます。/ Open a terminal.  
            2. 以下のコマンドを実行します。`<YOUR_GROQ_API_KEY>`をあなたのAPIキーに置き換えてください。/ Run this command, replacing `<YOUR_GROQ_API_KEY>` with your API key:  
                ```bash
                export GROQ_API_KEY="<YOUR_GROQ_API_KEY>"
                ```  
            3. この設定はターミナルを閉じるまで有効です。永続化するには、`.bashrc`や`.zshrc`に追記します。/ This lasts until the terminal closes. For persistence, add it to `.bashrc` or `.zshrc`.

### 使用方法 / Usage
1.  **スクリプトを実行 / Run the Script**:  
    ```bash
    python main.py
    ```  

2.  **表示されるメニューから操作を選択 / Select an Option from the Menu**:  
    1. 新しいプロンプトと結果を保存 / Save a new prompt and result  
    2. 保存済みのファイルを読み込む / Load a saved file  
    3. 保存済みのファイルを編集 / Edit a saved file  
    4. プログラムを終了 / Exit the program  
    指示に従い、プロンプトや追加情報を入力します。/ Follow the instructions to input prompts or additional info.

### 保存データの形式 / Saved Data Format
**保存されるJSONファイルの例 / Example of a saved JSON file**:  
```json
{
  "service_name": "llama3-70b-8192",
  "input_info": "親しみやすいトーン",
  "timestamp": "2025-02-22T10:00:00",
  "prompt": "こんにちは！",
  "result": "こんにちは、お元気ですか？",
  "history": [
    {
      "timestamp": "2025-02-22T09:50:00",
      "prompt": "こんにちは",
      "result": "こんにちは！",
      "input_info": "カジュアル",
      "old_service_name": "llama3-70b-8192",
      "new_service_name": "llama3-70b-8192"
    }
  ]
}
