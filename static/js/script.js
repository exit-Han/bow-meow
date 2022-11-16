/*details script*/
$(document).ready(function () {
  show_comment();
});

function save_comment() {
  let post_id = $("#object_id").val();
  let name = $("#name").val();
  let comment = $("#comment").val();

  $.ajax({
    type: "POST",
    url: "/comments",
    data: {
      postId_give: post_id,
      nickname_give: name,
      comment_give: comment,
    },
    success: function (response) {
      alert(response["msg"]);
      window.location.reload();
    },
  });
}

function show_comment() {
  $.ajax({
    type: "GET",
    url: "/comments",
    data: {},
    success: function (response) {
      let rows = response["lists"];
      for (let i = 0; i < rows.length; i++) {
        let nickname = rows[i]["nickname"];
        let comment = rows[i]["comment"];

        let temp_html = `<div class="card">
                                            <div class="card-body">
                                                <blockquote class="blockquote mb-0">
                                                    <p>${comment}</p>
                                                    <footer class="blockquote-footer">${nickname}</footer>
                                                </blockquote>
                                            </div>
                                        </div>`;
        $("#comment-list").append(temp_html);
      }
    },
  });
}
/*end of detatils script*/
