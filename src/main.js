const { readResults } = require('./readResults');
const { createTable } = require('./createTable');
const { summary } = require('@actions/core/lib/summary');
const github = require('@actions/github');

async function postJobSummary(results) {
    const message = createTable(results);
    await summary.addRaw(message).write();
}

async function run() {
    const results = readResults();

    await postJobSummary(results);
    
    const octokit = github.getOctokit(process.env.GITHUB_TOKEN);
    const context = github.context;

    const comment = createTable(results);
    
    // Verifica se o evento foi de um Pull Request (pr)
    if (context.payload.pull_request) {
        await octokit.rest.issues.createComment({
            ...context.repo,
            issue_number: context.payload.pull_request.number,
            body: comment
        });
    } else {
        await octokit.rest.repos.createCommitStatus({
            ...context.repo,
            sha: context.sha,
            state: 'success',
            description: 'Scan results posted.',
            context: '2ms Scan Results'
        });
    }
}

run().catch((error) => {
    console.error('Error posting job summary:', error);
});
