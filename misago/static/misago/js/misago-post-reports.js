// Controller for reporting posts
$(function() {

  MisagoPostReports = function(post) {

    this.post = post;
    this.api_url = post.$e.data('reports-url');
    this.is_open = false;

    this.$e = null

    var _this = this;

    this.open = function(api_url) {

      if (!this.is_open) {

        $.get(api_url, function(data) {

          this.is_open = true;
          this.$e = _this.post.$reports;

          this.$e.html(data);

        });

      }

    }
    this.open(this.api_url);

  }

  Misago.PostReports = MisagoPostReports;

});
