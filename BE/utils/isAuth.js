// this function will protect backend routes from being accessed by unauthenticated users
function isAuthenticated(req, res, next) {
  if (req.user) return next();
  res.status(401).json({
    message: 'You must login first',
  });
}

module.exports = isAuthenticated;
