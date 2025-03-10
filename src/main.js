require('dotenv').config();  

const fs = require("fs");
const core = require("@actions/core");
const github = require("@actions/github");
const path = require("path");
const { createComment } = require("./report"); 

const repo = {
  owner: process.env.GITHUB_REPOSITORY.split('/')[0], 
  repo: process.env.GITHUB_REPOSITORY.split('/')[1],   
};

const commitSha = process.env.GITHUB_SHA || github.context.sha;  
const token = process.env.GITHUB_TOKEN; 

console.log("GITHUB_TOKEN:", token);  

async function postCommitComment(results, commitSha, repo) {
  try {
    const message = createComment(results);

    const octokit = github.getOctokit(token);  

    await octokit.rest.repos.createCommitComment({
      ...repo,
      commit_sha: commitSha,
      body: message,
    });
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

    // O commitSha já está sendo carregado acima via process.env.GITHUB_SHA
    // Não é necessário redefinir aqui

    // Chama a função para postar o comentário no commit
    await postCommitComment(results, commitSha, repo);

  } catch (error) {
    core.setFailed(`Workflow error: ${error.message}`);
  }
}

run();
