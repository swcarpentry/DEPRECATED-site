---
layout: blog
root: ../../..
author: Raniere Silva
title: "Yet Another Template for Lessons"
date: 2014-10-11
time: "10:00:00"
category: ["Tooling"]
---
<!-- start excerpt -->
<p>After the <a href="{{page.root}}/blog/2014/09/splitting-the-repo.html">splitting the repository post</a>, Gabriel A. Devenyi and Greg Wilson wrote some suggestions for how the new lessons repositories should look like. <a href="{{page.root}}/blog/2014/10/of-templates-and-metadata.md">Gabriel's post</a> focus on metadata and <a href="{{page.root}}/blog/2014/10/a-new-template-for-lessons.md">Greg's post</a> on the file structure. From my experience on Mozilla Science Lab sprint I don't like Gabriel's <code>preq</code> metadata because I don't believe it helps very much. On Greg's proposal I didn't like the duplicate of some files at every git repository. Here is some changes that I suggest.</p>
<!-- end excerpt -->
<h2 id="design-choices">Design Choices</h2>
<p>In addition to Greg's design choices:</p>
<ul>
<li><p>Avoid, as much as possible, the duplication of files across git repositories.</p>
On Greg's proposal the git repositories should store CSS and Javascript files needed to properly render the page. We could avoid it.</li>
<li><p>Only automatize the actions that users and developers will need to do very often.</p>
<p>We <a href="https://github.com/swcarpentry/bc/pull/415">try to automatize workshops' home page</a> but we are going to revert it. For that reason I think we should wait people complains about the lack of some script before we wrote it.</p></li>
</ul>
<h2 id="git-repositories">Git Repositories</h2>
<p>The lesson repositories must have two branches: <code>master</code> and <code>gh-pages</code>. The <code>master</code> branch will store the lessons in Markdown (or any other format, that can be convert to HTML, wanted by the community). The <code>gh-pages</code> branch will store the HTML version of the lesson so that students can view it online.</p>
<p>We had exactly this approach until a few weeks ago in <code>bc</code> repo. Why back? At <code>bc</code> we only merge <code>master</code> into <code>gh-pages</code> a few times and I would like to suggest that the topic manintainers do it before the <a href="{{page.root}}/blog/2014/09/sept-2014-lab-meeting-report.html">in-service days proposed at last month meeting</a>.</p>
<p>Also, this approach will avoid the problem of have Markdown and HTML side-by-side since Markdown extensions support by Pandoc aren't supported by Jekyll.</p>
<h2 id="overall-layout-for-master-branch">Overall Layout for master branch</h2>
<p>Changes to Greg's layout:</p>
<ul>
<li>Drop of <code>glossary.md</code> in favor of link words to Wikipedia articles.</li>
<li><p>Drop of <code>web/</code> to avoid duplication of files across repositories.</p>
Web resources, such as CSS files, icons, and Javascript, can be provided by a &quot;third-party&quot; server.</li>
<li><p>Drop of <code>_layouts/</code> and <code>_includes</code>. To avoid duplication of files across repositories.</p>
<code>Makefile</code> will download the needed files from a &quot;third-party&quot; server when needed.</li>
<li><p>Drop of <code>bin/</code>. To avoid duplication of files across repositories and scripts that no one will use.</p>
<p>In case we need some tool for managing lessons it should live in its own repository and we should ask contributors to install it.</p></li>
</ul>
<h2 id="software-and-data">Software and Data</h2>
<p>I suggest to drop <code>code/index.md</code> and <code>data/index.md</code> to avoid the work of keep them update. Contributors can find the &quot;description&quot; of the files inside <code>code/</code> and <code>data/</code> using</p>
<pre><code>$ grep &#39;filename.ext&#39; *.md</code></pre>
<h2 id="overall-makefile">Overall Makefile</h2>
<p>Changes to Greg's proposal:</p>
<ul>
<li>Drop <code>make topic dd-slug</code> because is easy to copy one of the previous topics and correct the file names if needed.</li>
<li><code>make check</code> should run <code>swc-lesson-check</code> that need to be installed.</li>
<li><code>make site</code> download the necessary files (e.g. <code>_layouts</code> and <code>_includes</code>) and after it build the lesson website locally for previewing.</li>
<li>Drop <code>make summary</code>.</li>
<li><code>make release</code>: update <code>gh-pages</code> based on <code>master</code>. <strong>This should be only used by topic maintainers</strong>.</li>
</ul>
