/*
 * Date Format 1.2.3
 * (c) 2007-2009 Steven Levithan <stevenlevithan.com>
 * MIT license
 *
 * Includes enhancements by Scott Trenda <scott.trenda.net>
 * and Kris Kowal <cixar.com/~kris.kowal/>
 *
 * Accepts a date, a mask, or a date and a mask.
 * Returns a formatted version of the given date.
 * The date defaults to the current date/time.
 * The mask defaults to dateFormat.masks.default.
 */

 var dateFormat = function () {
 	var	token = /d{1,4}|m{1,4}|yy(?:yy)?|([HhMsTt])\1?|[LloSZ]|"[^"]*"|'[^']*'/g,
 	timezone = /\b(?:[PMCEA][SDP]T|(?:Pacific|Mountain|Central|Eastern|Atlantic) (?:Standard|Daylight|Prevailing) Time|(?:GMT|UTC)(?:[-+]\d{4})?)\b/g,
 	timezoneClip = /[^-+\dA-Z]/g,
 	pad = function (val, len) {
 		val = String(val);
 		len = len || 2;
 		while (val.length < len) val = "0" + val;
 		return val;
 	};

	// Regexes and supporting functions are cached through closure
	return function (date, mask, utc) {
		var dF = dateFormat;

		// You can't provide utc if you skip other args (use the "UTC:" mask prefix)
		if (arguments.length == 1 && Object.prototype.toString.call(date) == "[object String]" && !/\d/.test(date)) {
			mask = date;
			date = undefined;
		}

		// Passing date through Date applies Date.parse, if necessary
		date = date ? new Date(date) : new Date;
		if (isNaN(date)) throw SyntaxError("invalid date");

		mask = String(dF.masks[mask] || mask || dF.masks["default"]);

		// Allow setting the utc argument via the mask
		if (mask.slice(0, 4) == "UTC:") {
			mask = mask.slice(4);
			utc = true;
		}

		var	_ = utc ? "getUTC" : "get",
		d = date[_ + "Date"](),
		D = date[_ + "Day"](),
		m = date[_ + "Month"](),
		y = date[_ + "FullYear"](),
		H = date[_ + "Hours"](),
		M = date[_ + "Minutes"](),
		s = date[_ + "Seconds"](),
		L = date[_ + "Milliseconds"](),
		o = utc ? 0 : date.getTimezoneOffset(),
		flags = {
			d:    d,
			dd:   pad(d),
			ddd:  dF.i18n.dayNames[D],
			dddd: dF.i18n.dayNames[D + 7],
			m:    m + 1,
			mm:   pad(m + 1),
			mmm:  dF.i18n.monthNames[m],
			mmmm: dF.i18n.monthNames[m + 12],
			yy:   String(y).slice(2),
			yyyy: y,
			h:    H % 12 || 12,
			hh:   pad(H % 12 || 12),
			H:    H,
			HH:   pad(H),
			M:    M,
			MM:   pad(M),
			s:    s,
			ss:   pad(s),
			l:    pad(L, 3),
			L:    pad(L > 99 ? Math.round(L / 10) : L),
			t:    H < 12 ? "a"  : "p",
			tt:   H < 12 ? "am" : "pm",
			T:    H < 12 ? "A"  : "P",
			TT:   H < 12 ? "AM" : "PM",
			Z:    utc ? "UTC" : (String(date).match(timezone) || [""]).pop().replace(timezoneClip, ""),
			o:    (o > 0 ? "-" : "+") + pad(Math.floor(Math.abs(o) / 60) * 100 + Math.abs(o) % 60, 4),
			S:    ["th", "st", "nd", "rd"][d % 10 > 3 ? 0 : (d % 100 - d % 10 != 10) * d % 10]
		};

		return mask.replace(token, function ($0) {
			return $0 in flags ? flags[$0] : $0.slice(1, $0.length - 1);
		});
	};
}();

// Some common format strings
dateFormat.masks = {
	"default":      "ddd mmm dd yyyy HH:MM:ss",
	shortDate:      "m/d/yy",
	mediumDate:     "mmm d, yyyy",
	longDate:       "mmmm d, yyyy",
	fullDate:       "dddd, mmmm d, yyyy",
	shortTime:      "h:MM TT",
	mediumTime:     "h:MM:ss TT",
	longTime:       "h:MM:ss TT Z",
	isoDate:        "yyyy-mm-dd",
	isoTime:        "HH:MM:ss",
	isoDateTime:    "yyyy-mm-dd'T'HH:MM:ss",
	isoUtcDateTime: "UTC:yyyy-mm-dd'T'HH:MM:ss'Z'"
};

// Internationalization strings
dateFormat.i18n = {
	dayNames: [
	"Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat",
	"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"
	],
	monthNames: [
	"Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
	"January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"
	]
};

// For convenience...
Date.prototype.format = function (mask, utc) {
	return dateFormat(this, mask, utc);
};

Date.prototype.addHours = function(h){
	this.setHours(this.getHours()+h);
	return this;
};

String.prototype.trunc = function(n, useWordBoundary){
    var toLong = this.length > n,
        s_ = toLong ? this.substr(0,n-1) : this;
    s_ = useWordBoundary && toLong ? s_.substr(0,s_.lastIndexOf(' ')) : s_;
    return  toLong ? s_ + '&hellip;' : s_;
};

function getURLParameter(name) {
    return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search)||[,""])[1].replace(/\+/g, '%20'))||null;
}

function getTrimmedQueryString() {
    return $.trim($('#s').val());
}

function buildURLQueryString(q, page_num, show_all, browse) {
    var query_dict = {}
    if (q) {
        query_dict['q'] = q;
    }
    if (browse) {
        query_dict['browse'] = 1;
    }
    if (page_num) {
        query_dict['page'] = + page_num;
    }
    if (show_all) {
        query_dict['all'] = 1;
    }

    query_string = '?' + $.param(query_dict);
    return query_string;
}

$(document).ready(function(){
    largeScreenPlaceholder = true;
    resizePlaceholder();
    var q = getURLParameter('q');
    var browse = getURLParameter('browse');
    if (q || browse) {
        transition_to_result_mode();
        $('#s').val(q);
        perform_search_query(q, getURLParameter('page'), getURLParameter('all'), browse);
        if (q) {
            perform_suggested_query(q);
        } else if (browse) {
            var result_list = $("div.recommend-results ol.result-list");
            result_list.empty();
            result_list.hide();
        }
    } else {
        perform_search_query(undefined, undefined, undefined, true);
    }
});

function resizePlaceholder() {
    var width = $( window ).width();

    if (width > 479 && !largeScreenPlaceholder) {
        $('#s').attr("placeholder", "Search by session name, presenter, theme, etc.");
        largeScreenPlaceholder = true;
    } else if (width < 479 && largeScreenPlaceholder) {
        $('#s').attr("placeholder", "Search by session name");
        largeScreenPlaceholder = false;
    }
}

$( window ).resize(function() {
    resizePlaceholder();
});

$('#search_box').submit(function(e){
    var q = getTrimmedQueryString();
    History.pushState({query:q}, 'UpWord Notes SXSW', buildURLQueryString(q));
	e.preventDefault();
});

$('#s').on('input propertychange', function(){
    transition_to_result_mode();
});

$('body').on('click', 'p.more a', function(e) {
    var q = $(this).attr('query');
    History.pushState({query:q}, 'UpWord Notes SXSW', buildURLQueryString(q));
    $("body").animate({ scrollTop: 0 }, "fast");
	e.preventDefault();
});

$('p.show-hidden a').click(function(e){
    var q = $(this).attr('query'),
        page_num = $(this).attr('page'),
        show_all = true;
    History.pushState({query:q, page:page_num, showAll:show_all}, 'UpWord Notes SXSW', buildURLQueryString(q, page_num, show_all));
    e.preventDefault();
});

var result_mode = false;
function transition_to_result_mode() {
    if (!result_mode) {
        $('body').addClass('iresults');
        $('div.search-form').addClass('show-result');
        $('#wrapper').addClass('results');
        $('div.twitter-timeline-container').hide();
        result_mode = !result_mode;
        $('#s').autocomplete({
            serviceUrl: '/api/v1/event/auto/',
            paramName: 'q',
            minChars : 3,
            onSelect: function (suggestion) {
                $('#search_box').submit();
            }
        });
    }
}

function update_pagination(num_pages, page_num, q, show_all, browse) {
    if (num_pages == 0 || num_pages == 1) {
        $('div.pagination').pagination('destroy');
    } else {
        $('div.pagination').pagination({
            pages: num_pages,
            cssStyle: 'light-theme',
            edges : 1,
            currentPage: page_num || 1,
            displayedPages: 3,
            onPageClick: function(newPageNumber){
                History.pushState({query:q, page:newPageNumber, showAll:show_all, browse:browse}, 'UpWord Notes SXSW', buildURLQueryString(q, newPageNumber, show_all, browse));
                return false;
            }
        });
    }
}

function build_result_summary_text(total_num_events, total_num_notes) {
    var result_summary_text = '';
    if (total_num_events < 100) {
        result_summary_text = 'Browse ' + total_num_events + ' sessions';
    } else {
        result_summary_text = 'Browse 100+ sessions';
    }
    if (total_num_notes == 1) {
        result_summary_text += ' with 1 note';
    } else if (total_num_notes > 1) {
        result_summary_text += ' with ' + total_num_notes + ' notes';
    }
    return result_summary_text;
}

function build_num_notes_text(result_obj) {
    var num_notes_string = 'No notes yet, be the 1st to share';
    if (result_obj.num_notes == 1)  {
        num_notes_string = '1 Note Available';
    } else if (result_obj.num_notes > 1) {
        num_notes_string = '' + result_obj.num_notes + ' Notes Available';
    }
    return num_notes_string;
}

function build_presenter_text(result_obj) {
    var presenters_string = '';
    if (result_obj.presenter.length > 0) {
        var presenter_full = _.map(result_obj.presenter, function(presenter){
            if (presenter.company) {
                return presenter.name + ' (' + presenter.company + ')';
            } else {
                return presenter.name;
            }
        });
        if (presenter_full.length == 1) {
            presenters_string = 'Presenter: ';
        } else {
            presenters_string = 'Presenters: ';
        }
        presenters_string += presenter_full.join(', ').trunc(90, true);
    }
    return presenters_string;
}

/*
 * Search result underscore template
 */
 var search_result_template = _.template('<li class="result"> \
 	<div class="data-time"><%= start_time %></div> \
    <% if (num_notes == 0) { %> \
     	<h3 class="no-note"><%= title %></h3> \
        <div class="meta-data"><a href="http://upword-notes.tumblr.com/post/78600992601/shareyoursxswnotes"><span class="note-count no-note"><%= num_notes_text %></span></a>\
    <% } else { %> \
     	<h3><a href="<%= twitter_url %>"><%= title %></a></h3> \
     	<div class="meta-data"><a href="<%= twitter_url %>"><span class="note-count"><%= num_notes_text %></span></a>\
    <% } %> \
    <a href="<%= twitter_hashtag_url %>"><span class="note-author"><%= hash_tag %></span></a></div> \
 	<p><%= description %></p> \
    <p><i><%= presenters_text %></i></p> \
    <% if (details_url) { %> \
        <p class="details"><a target="_blank" href="<%= details_url %>">Full event details >>></a></p> \
    <% } %> \
    <% if (theme) { %> \
        <p class="more"><a query="<%= theme %>" href="#<%= theme %>">More from theme: <%= theme %></a></p> \
    <% } else { %> \
     	<p class="more">&nbsp;</p> \
    <% } %> \
 	</li>');

/*
 * Search jquery AJAX
 */
var xhr;
function perform_search_query(query, page, showAll, browse) {
    showAll = showAll || false;
    var result_list = $("div.organic-results ol.result-list");
    result_list.fadeTo( "fast", 0.33 );

    if (query) {
        var url_string = "/api/v1/event/search/?format=json&q=" + encodeURIComponent($.trim(query));
        $('div.browse').hide();
    } else {
        $('div.browse').show();
        var url_string = "/api/v1/event/browse/?format=json";
    }
    if (!!page && page % 1 === 0) {
        url_string += '&page=' + page;
    }
    if (showAll) {
        url_string += '&showAll=true';
    }
    if (xhr && xhr.readyState != 4) {
        xhr.abort();
    }
    $('#s').autocomplete('hide');
    var t = setTimeout("$('div.spinner').show()", 100); // Using timeout of 100ms to delay showing spinner
    xhr = $.ajax({url:url_string,
        cache: false ,
 		success:function(result) {
            clearTimeout(t);
            $('#s').autocomplete('hide');
 			result_list.empty();
            var result_summary = $("p.found");
            update_pagination(result.meta.pages, page, query, showAll, browse);
 			if (result.meta.pages == 0) {
 				result_list.append('<li class="result"><p>No results</p></li>');
                result_summary.text('Found no matching sessions');
 			} else {
                result_summary.text(build_result_summary_text(result.meta.total_count, result.meta.total_num_notes));

 				for (var i = 0; i < result.objects.length; i++) {
 				    var obj = result.objects[i];

					// Take care of PST to CST offset
                    var datetime = new Date(obj.start_time);

					var search_result = search_result_template({
                        start_time : dateFormat(datetime, "h:MM tt, ddd"),
						details_url : obj.details_url,
						twitter_url : obj.twitter_url,
						title : obj.title,
                        num_notes : obj.num_notes,
						num_notes_text : build_num_notes_text(obj),
						hash_tag : obj.hash_tags,
						description : obj.description.trunc(300, true),
                        presenters_text : build_presenter_text(obj),
						theme : obj.theme,
                        twitter_hashtag_url : obj.hashtag_url
					});

                    // Add to result_list html
					result_list.append(search_result);
         		}
    		}

            if ((result.meta.page == result.meta.pages || result.meta.pages == 0) && result.meta.hidden_count > 0) {
                $('div.hidden-events').show();
                $('p.hidden-summary').text("Hiding " + result.meta.hidden_count + " sessions that match your search, but don't have notes yet.");
                $('p.show-hidden a').attr('query', query).attr('page', page);

            } else {
                $('div.hidden-events').hide();
            }

            result_list.fadeTo( "fast", 1 );
            $('div.spinner').hide();

            if (!!page) {
                $("body").animate({ scrollTop: 0 }, "fast");
            }
	 	},
        error: function(jqXHR, textStatus, errorThrown) {
            clearTimeout(t);
            if (jqXHR.status === 0 || jqXHR.readyState === 0) {
                // aborted...do nothing
            } else {
                $('#s').autocomplete('hide');
                result_list.empty();
                result_list.append('<li class="result"><p>An error occurred. Please try again.</p></li>');
                result_list.fadeTo( "fast", 1 );
                $('div.spinner').hide();
                $("p.found").text('Found no matching sessions');
            }
        }
	});
}

var xhr_suggest;
function perform_suggested_query(query) {
    var result_list = $("div.recommend-results ol.result-list");
    result_list.fadeTo( "fast", 0.33 );

    var url_string = "/api/v1/event/?suggested=1&q=" + encodeURIComponent($.trim(query));
    if (xhr_suggest && xhr_suggest.readyState != 4) {
        xhr_suggest.abort();
    }
    xhr_suggest = $.ajax({url:url_string,
        cache: false,
 		success:function(result) {
 			if (result.meta.total_count > 0) {
                result_list.empty();
                $('div.recommend-results').show();

 				for (var i = 0; i < result.objects.length; i++) {
 				    var obj = result.objects[i];

					// Take care of PST to CST offset
                    var datetime = new Date(obj.start_time);

					var suggested_result = search_result_template(
						{  start_time : dateFormat(datetime, "h:MM tt, ddd"),
						details_url : obj.details_url,
						twitter_url : obj.twitter_url,
						title : obj.title,
                        num_notes : obj.num_notes,
						num_notes_text : build_num_notes_text(obj),
						hash_tag : obj.hash_tags,
						description : obj.description.trunc(300, true),
                        presenters_text : build_presenter_text(obj),
						theme : obj.theme,
                        twitter_hashtag_url : obj.hashtag_url
					});

                    // Add to result_list html
					result_list.append(suggested_result);
         		}
    		}
            result_list.fadeTo( "fast", 1 );
	 	},
        error: function(jqXHR, textStatus, errorThrown) {
            if (jqXHR.status === 0 || jqXHR.readyState === 0) {
                // aborted...do nothing
            } else {
                result_list.empty();
                result_list.fadeTo( "fast", 1 );
            }
        }
	});
}

(function(window, $){
    History.Adapter.bind(window,'statechange',function(){
        var State = History.getState();
        if (State.data.query || State.data.browse) {
            $('#s').val(State.data.query);
            perform_search_query(State.data.query, State.data.page, State.data.showAll, State.data.browse);

            if (State.data.page) {
                $("body").animate({ scrollTop: 0 }, "fast");
            } else if (State.data.browse) {
                var result_list = $("div.recommend-results ol.result-list");
                result_list.empty();
                result_list.hide();
            } else {
                perform_suggested_query(State.data.query);
            }
        } else {
            perform_search_query(undefined, undefined, undefined, true);
            $('div.hidden-events').hide();
        }
    });
})(window, $);