module.exports = {
  branches: ['main'], // Replace 'main' with your default branch if different
  plugins: [
    '@semantic-release/commit-analyzer', // Analyze commit messages
    '@semantic-release/release-notes-generator', // Generate release notes
    '@semantic-release/changelog', // Update changelog file
    '@semantic-release/npm', // Publish to npm (optional)
    '@semantic-release/github', // Create GitHub releases
    '@semantic-release/git', // Push updated files back to the repository
  ],
};