const fs = require("fs");
const core = require("@actions/core");
const github = require("@actions/github");
const path = require("path");
const { createComment } = require("./report");

const commitSha = github.context.sha;  // Obtém diretamente do contexto do GitHub
const token = process.env.GITHUB_TOKEN;  // A variável GITHUB_TOKEN é automaticamente fornecida pelo GitHub

async function postCommitComment(results, commitSha, repo) {
  try {
    const message = createComment(results);  

    const octokit = github.getOctokit(token);  

    
    await octokit.rest.repos.createCommitComment({
      ...repo,
      commit_sha: commitSha,
      body: message,
    });

    console.log("Adicionando Job Summary...");
    
    await core.summary
    .addRaw(message)  
    .write(); 
    
    console.log("Job Summary gerado com sucesso!");
    
  } catch (error) {
    core.setFailed(`Error posting commit comment: ${error.message}`);
  }
}

async function run() {
  try {
    const resultsPath = path.join(process.cwd(), "results/results.json");

    if (!fs.existsSync(resultsPath)) {
      core.setFailed("Results file not found in 'results/' folder.");
      return;
    }

    const results = JSON.parse(fs.readFileSync(resultsPath, "utf8"));

    const repo = github.context.repo; 
    await postCommitComment(results, commitSha, repo);

  } catch (error) {
    core.setFailed(`Workflow error: ${error.message}`);
  }
}

run();
