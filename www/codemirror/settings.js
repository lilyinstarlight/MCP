CodeMirror.defineMode("settings", function() {
  return {
    token: function(stream, state) {
      var sol = stream.sol() || state.afterSection;
      var eol = stream.eol();

      state.afterSection = false;

      if (sol) {
        if (state.nextMultiline) {
          state.inMultiline = true;
          state.nextMultiline = false;
        } else {
          state.position = "keyword";
        }
      }

      if (eol && ! state.nextMultiline) {
        state.inMultiline = false;
        state.position = "keyword";
      }

      if (sol) {
        while(stream.eatSpace());
      }

      var ch = stream.next();

      if (sol && (ch === "#")) {
        state.position = "comment";
        stream.skipToEnd();
        return "comment";
      } else if (ch === " ") {
        state.position = "quote";
        return null;
      } else if (ch === "\\" && state.position === "quote") {
        if (stream.next() !== "u") {    // u = Unicode sequence \u1234
          // Multiline value
          state.nextMultiline = true;
        }
      }

      return state.position;
    },

    startState: function() {
      return {
        position : "keyword",       // Current position, "keyword", "quote" or "comment"
        nextMultiline : false,  // Is the next line multiline value
        inMultiline : false,    // Is the current line a multiline value
        afterSection : false    // Did we just open a section
      };
    }

  };
});
