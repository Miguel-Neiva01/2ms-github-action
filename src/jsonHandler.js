const moment = require('moment');
const { summary } = require('@actions/core/lib/summary');

function createComment(results) {
    let message = "### 2ms Scan Summary\n";
    message += `**2msversion**: ${results['2ms-version']}\n\n`;

    message += `Total files scanned: **${results['files_scanned']}**\n`;

    return message;
}

async function postJobSummary(results) {
    const message = createComment(results);
    await summary.addRaw(message).write(); 
}

module.exports = {
    postJobSummary
};
