---
title: "Day 3: How to Use Try Hack Me—Commands, Questions, and Practical Lab Walkthrough"
date: 2026-01-03 11:30:00 +0530
categories: [Tutorials, Ethical Hacking]
tags: [tryhackme, linux, commands, beginners, ctf]
author: ayushjha
image:
  path: /assets/img/posts/20260103/1-thm-lab-desk-setup.png
  alt: "Stylized top-down view of a cybersecurity lab desk setup."
---

### Introduction: Learning Try Hack Me by Actually Using It

After completing the account setup on Day 1 and understanding the Welcome Lab on Day 2, Day 3 moves into real interaction with the Try Hack Me lab environment. In this blog, the focus is on the “How to Use Try Hack Me” room, where beginners learn how to operate inside a live machine, execute Linux commands, and answer task-based questions correctly.

This room is extremely important because it teaches how Try Hack Me labs actually work in practice. Instead of theory, learners execute real commands in a terminal and observe real outputs. The attached screenshot clearly demonstrates this interaction, showing commands being executed and answers being validated.

![The Try Hack Me lab interface showing the room details.](/assets/img/posts/20260103/2-thm-room-interface.png)
_The "How to use TryHackMe" room interface._


### Understanding the Try Hack Me Lab Interface

In the “How to Use Try Hack Me” room, the screen is divided into two main sections. The left-hand side contains the task instructions and questions, while the right-hand side displays the live Linux terminal of the tutorial machine. This layout allows learners to read instructions and immediately apply them, which mirrors real-world cybersecurity workflows. The uploaded screenshot shows this exact layout, with task progress visible on the left and command execution happening on the right.

![Executing the 'ls' command in the Try Hack Me terminal.](/assets/img/posts/20260103/3-thm-ls-command.png)
_Initial 'ls' command reveals the 'testdir' directory._

### Command 1: Listing Files Using `ls`

The first command used in the lab is `ls`. This command is used to list all files and directories present in the current working directory. When the command `ls` is executed in the terminal, the output shows a directory named `testdir`. This command helps learners understand how to inspect the contents of a directory, which is a foundational Linux skill used in almost every cybersecurity lab.

**Question Asked:**
> What is the name of the folder you see?

**Correct Answer:**
The folder name displayed is `testdir`, which is submitted in the answer field and marked correct, as shown in the screenshot.

![Navigating into the 'testdir' directory.](/assets/img/posts/20260103/4-thm-cd-command.png)
_Successfully changing the directory into 'testdir'._

### Command 2: Changing Directory Using `cd testdir`

After identifying the folder, the next command used is `cd testdir`. The `cd` command stands for *change directory* and is used to move from the current directory into another directory. Executing this command moves the terminal session inside the `testdir` folder. This step teaches learners how directory navigation works in Linux, which is essential when exploring file systems during penetration testing or forensic analysis.

**Question Asked:**
> Like you would open a folder on your Desktop, you can change directory (moving folders) by typing "cd <location>". Move into the folder you just found.

**Answer Requirement:**
No answer is required for this step, as the task is purely action-based. Successfully executing the command allows the learner to proceed.

![Listing and reading the contents of 'hello.txt'.](/assets/img/posts/20260103/5-thm-cat-command-sequence.png)
_The full command sequence to find and read the file._

### Command 3: Listing Files Again Using `ls`

Once inside the `testdir` directory, the `ls` command is used again. This time, a file named `hello.txt` is displayed. This reinforces the idea that the `ls` command lists contents relative to the current directory. Using `ls` repeatedly to understand directory structure is a habit that every cybersecurity professional develops over time.

### Command 4: Reading File Content Using `cat hello.txt`

The next command executed in the lab is `cat hello.txt`. The `cat` command is used to display the contents of a file directly in the terminal. When this command is executed, the output displayed is “hacking labs”. This step introduces learners to file inspection, which is a critical skill in cybersecurity when reviewing logs, configuration files, or scripts.

**Question Asked:**
> We can see a files content by typing "cat <filename>". List the files in the folder you are in, what is content of the hello.txt file?

**Correct Answer:**
The correct answer is `hacking labs`, which is entered into the answer field and confirmed as correct.

![The Try Hack Me interface showing correct answers validated.](/assets/img/posts/20260103/6-thm-answer-validation.png)
_Correct answers are validated in real-time._


### Final Instruction: Terminating the Machine

At the end of the task, Try Hack Me instructs learners to stop the running machine by clicking the **Terminate** button. This step does not require an answer, but it is extremely important. Properly terminating machines ensures responsible resource usage and reflects professional lab discipline. Developing this habit early prepares learners for real-world lab environments where unmanaged resources can lead to security and performance issues.


### Understanding Answer Validation in Try Hack Me

Each time an answer is submitted, Try Hack Me provides instant feedback. Correct answers are highlighted and marked clearly, helping learners confirm their understanding. This immediate validation is one of the strongest features of the platform, as it reinforces learning through real-time confirmation.

![The machine information panel with the Terminate button highlighted.](/assets/img/posts/20260103/8-thm-terminate-machine.png)
_Always remember to terminate your machine after use._


### Day 3 Learning Outcome

By completing Day 3, learners gain hands-on experience with the Try Hack Me lab interface, understand how to execute Linux commands inside a virtual machine, and learn how to answer task-based questions correctly. The commands `ls`, `cd`, and `cat` form the foundation of Linux navigation and file inspection, which are used repeatedly throughout cybersecurity labs. This day represents the true starting point of practical cybersecurity learning.

![The completion screen for the 'How to use TryHackMe' room.](/assets/img/posts/20260103/9-thm-room-complete.png)
_Success! The introductory room is complete._

### Day 4 Preview: Hello Lab

On Day 4, the series will move to the **Hello Lab**, where learners will further strengthen their interaction with Try Hack Me labs. This room will build confidence by reinforcing basic command execution and task understanding, preparing learners for more technical Linux and security-focused challenges ahead.

### Conclusion

The "How to Use Try Hack Me” room is a critical milestone for beginners. It transforms theoretical understanding into real execution by introducing live machines, terminal commands, and task-based validation. Mastering these basics ensures that future cybersecurity labs are approached with clarity and confidence. Stay consistent, stay curious, and keep learning—because cybersecurity mastery begins with understanding the basics.

> "The first rule of cybersecurity: trust nothing, verify everything."



**—Mr. Xploit** 🛡️

