# GitHub Copilot Demos and Shortcuts


## Introduction
This repository contains demos and shortcuts for using GitHub Copilot effectively. GitHub Copilot is an AI-powered code completion tool that helps you write code faster and smarter.

## Demos
1. **Basic Code Completion**
    - Demonstrates how GitHub Copilot can complete code snippets based on the context.
    
2. **Function Suggestions**
    - Shows how GitHub Copilot suggests entire functions based on the function name and comments.
    
3. **Code Refactoring**
    - Example of how GitHub Copilot can help refactor existing code for better readability and performance.

## Shortcuts
- **Trigger Suggestions**: `Ctrl + Space` (Windows/Linux) or `Cmd + Space` (Mac)
- **Accept Suggestion**: `Tab` or `Enter`
- **Cycle Through Suggestions**: `Alt + ]` and `Alt + [` (Windows/Linux) or `Ctrl + ]` and `Ctrl + [` (Mac)
- **Dismiss Suggestion**: `Esc`

## Getting Started
To get started with GitHub Copilot, follow these steps:
1. Install the GitHub Copilot extension for your code editor (e.g., Visual Studio Code).
2. Open a new or existing file in your project.
3. Start typing and let GitHub Copilot assist you with code suggestions.

## Resources
- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [GitHub Copilot FAQ](https://github.com/github/feedback/discussions/categories/copilot)

## Contributing
If you have any demos or shortcuts to add, feel free to open a pull request or create an issue.

## License
This project is licensed under the MIT License.
## Additional Use Cases

1. **Assisting Non-Native English Speakers**
    GitHub Copilot can understand other languages beyond English! This is helpful for developers of all backgrounds because programming languages are based on American English. For example, the CSS property color is based on American English, so it is unfamiliar for native British-English or Canadian-English speakers who use the spelling ‘colour’. Forgetting the correct spelling and syntax can often result in typos, unexpected errors, and lost time.

    In the GIF below, I wrote a comment in Spanish that says, “importar,” which translates to “import.” GitHub Copilot quickly completed my comment in Spanish and imported the necessary libraries as the comment described.

2. **Creating Dictionaries with Lookup Data**
    Martin Woodward, Vice President of Developer Relations at GitHub, shared this tip with us! GitHub Copilot is great at creating dictionaries of lookup data. Try it out by writing a comment instructing GitHub Copilot to create a dictionary of two-letter ISO country codes and their contributing country name. Writing a comment and the first few lines of code should help GitHub Copilot generate the desired results. See the GIF below for visual representation!

3. **Testing Your Code**
    Writing tests is a vital yet sometimes tedious step in the software development lifecycle. Because GitHub Copilot excels in pattern recognition and pattern completion, it can speed up the process of writing unit tests, visual regression tests, and more.

4. **Matching Patterns with Regular Expressions**
    With GitHub Copilot, you can spend less time fiddling in a Regex playground or combing through StackOverflow to match character combinations in strings. Instead, you can write a comment or a function name to trigger GitHub Copilot’s suggestions.

    I used Copilot to help me validate a phone number!

5. **Preparing for Technical Interviews**
    While this may sound unorthodox, developers, including myself, use GitHub Copilot to study for interviews.

    Here’s the strategy:
    - First, I try to solve the problem without GitHub Copilot.
    - If I’m feeling extremely stuck and disheartened while solving the problem, I’ll activate GitHub Copilot and use it to generate ideas on how to solve the problem better.
    - Subsequently, I’ll delete the code GitHub Copilot generated, deactivate GitHub Copilot, and make another attempt at finding a solution with the new information in mind.

6. **Sending Tweets**
    Of course, you can simply use the Twitter application to send a Tweet, but it’s more fun to send a Tweet via your IDE! As a Developer Advocate, part of my job is to create demos. In a recent livestream, I had to demonstrate using Twitter API v2 with GitHub Copilot in Python, a language that I rarely use. GitHub Copilot saved the day and generated the code I needed after I wrote a few comments. Read my DEV post if you want to try sending a tweet with GitHub Copilot, too!

7. **Exiting Vim**
    Developers who are new to Vim frequently wonder how to exit the editor. Struggling to exit vim is so common that it’s a meme on the internet! Since GitHub Copilot is available in Visual Studio Code, JetBrains, and Neovim, a forked version of Vim with additional features, you can exit NeoVim using GitHub Copilot. In the video below, Brian Douglas uses GitHub Copilot to exit NeoVim, by writing a comment that says, “How do I exit vim?”

8. **Navigating a New Codebase with Copilot Labs**
    GitHub Copilot Labs is a complementary extension that comes with GitHub Copilot access. The GitHub Next team developed GitHub Copilot Labs, an experimental sidebar, to help developers translate code from one programming language to another and get a step-by-step explanation of code snippets.

    There’s no easy method for building a mental model of a new codebase, but these two features within GitHub Copilot Labs can help. By translating code snippets to languages they’re more familiar with and using the ‘Explain’ feature to gain an understanding of the code, developers can better comprehend complex blocks of code.