const moment = require('moment');
const { summary } = require('@actions/core/lib/summary');

function createComment(results) {
    let message = `\n**2ms version: ${results['version']}**\n`;  

    message += "<table>\n";
    message += "<tr></tr>\n";
    message += "<tr><td>\n\n";

    message += "| Metric | Values |\n";
    message += "| --- | --- |\n";
    message += `| Files scanned | ${results['files_scanned']}\n`;
    message += `| Files parsed | ${results['files_parsed']}\n`;
    message += `| Files failed to scan | ${results['files_failed_to_scan']}\n`;
    message += `| Execution time | ${moment(results['end']).diff(moment(results['start']), 'seconds')} seconds\n`;

    message += "\n</td></tr>\n</table>\n\n";

    return message;
}

async function postJobSummary(results) {
    const message = createComment(results);
    await summary.addRaw(message).write();
}

module.exports = {
    postJobSummary
};
