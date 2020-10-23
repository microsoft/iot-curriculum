# Lab contribution guidelines

We ❤️ contributions! We'd love you to share your labs with us so we can provide as much great content as possible to students and educators around the world.

## Ways to contribute

There are three ways you can contribute:

* **Find/fix issues:**
  We do our best to ensure this content is good, correct, and up to date, but we are only human. There may be mistakes, missed information, or the technology may have moved on and changed. If you find any problems with the labs either [raise an issue](https://github.com/microsoft/iot-curriculum/issues), or even better, fork the repo, fix the problem and raise a [pull request](https://github.com/microsoft/iot-curriculum/pulls).

* **Suggest labs:**
  If there are labs you'd like to have included, maybe it's something your students would need, or a lab you have already created somewhere else then let us know. [Raise an issue](https://github.com/microsoft/iot-curriculum/issues) with details on the content you want, or a link to existing content you'd like in this repo and we'll work with you to get it created or ported over.

* **Submit your own labs:**
If you already have a lab you'd like to include, then please fork the repo, fix the problem and raise a [pull request](https://github.com/microsoft/iot-curriculum/pulls) adding the lab into this folder. We'll review it, work through any changes we need with you and help get it in. All contributions will need to follow the content guidelines below, as well as the requirements in our [Contributing guidelines](https://github.com/microsoft/iot-curriculum/blob/main/CONTRIBUTING.md).

## Content guidelines

We've put together these guidelines to help ensure the labs you contribute align with the rest of the content here.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/)
or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

* **Avoid duplication of core scenarios:**
  We want a wide variety of different scenarios covered. If you want to create a lab that is similar to an existing one, but using a different sensor or board then maybe consider expanding the existing one to mention both sensors instead of creating a whole new lab.

* **Point to Microsoft documentation or first party documentation instead of duplicating:**
  We have a lot of great content in [Microsoft docs](https://docs.microsoft.com?WT.mc_id=academic-7372-jabenn) and [Microsoft Learn](https://docs.microsoft.com/learn?WT.mc_id=academic-7372-jabenn), so there's no need to duplicate what's there. Not only does this apply to full guides, but even parts of a lab. For example, there's no need to document how to create a service if the relevant docs provide all the details - just link to the docs. This way there is less content to keep up to date, the docs team will update their content when it goes out of date.

  For example, in the [Environment Monitor](./iot/environment_monitor/), there are links to Raspberry Pi documentation to image SD cards, and Microsoft Docs to delete resource groups.

* **Think about your audience:**
  The audience for this content is a mixture of educators and students. It's great to have a mix of beginner and more advanced content, but it should be appropriate for education environments - so not need many years experience to understand, or have expensive requirements for Azure services or hardware unless it is a very specific scenario. For example, use free tiers of Azure services where possible, use programming languages students are likely to know (Python is a great choice as it is popular with students, Haskell is much less popular so not a good choice), use commodity hardware that's easily available from global suppliers and has good tooling.

* **Define in each lab the requirements:**
  At the start of each lab, add a header that shows who created it, the hardware and software needed, the Azure services used etc. You can see an example [in the OCR lab](./ai-edge/ocr/README.md) The fields required are:

  * Author - who wrote the lab with a link to their GitHub or other profiles
  * Target platform - the hardware this will run on
  * Hardware required - a full list of hardware required
  * Software required - a full list of software required (additional to what you would expect - for example, no need to mention an operating system unless the lab is operating system specific)
  * Azure Services - a list of the Azure services used
  * Programming Language - the programming language or languages used
  * Prerequisites - what the reader will need to know to work through the lab, such as proficiency in any programming languages or concepts
  * Date - the date the lab was created as month and year
  * Learning Objectives - what the reader will learn to do during this lab
  * Time to complete - a rough estimate of how long it would take an average student to complete this lab

* **Divide up long labs:**
  If your lab will take more than an hour, divide up the instructions into multiple steps, with each step having an objective that can be completed with an outcome that can be seen and gives a sense of achievement.

* **Provide clean up instructions:**
  At the end of each lab, provide instructions on how to clean up and Azure services created. This will help folks save money or Azure credit after completing the lab. Ensure all services are created in the same resource group to make this easier.
