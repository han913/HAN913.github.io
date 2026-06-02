const { getStore } = require("@netlify/blobs");

exports.handler = async () => {
  const store = getStore("graduation-album");
  const approved = await store.get("approved", { type: "json" }) || [];

  return {
    statusCode: 200,
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(approved)
  };
};