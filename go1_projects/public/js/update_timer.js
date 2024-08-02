frappe.provide("go1_projects.daily_update");

go1_projects.daily_update.timer = function(frm, row, timestamp=0) {
    let options = []
    for(let i of frm.doc.allocate_task){
		options.push(i.task+" - "+i.subject)
    }
	var new_options = new Set(options)
	options=[...new_options]
	let dialog = new frappe.ui.Dialog({
		title: __("Timer"),
		fields:
		[
			{"fieldtype": "Link", "label": __("Activity Type"), "fieldname": "activity_type",
				"reqd": 1, "options": "Activity Type"},
			{"fieldtype": "Select", "label": __("Task"), "fieldname": "task", "options": options,"reqd":1},
			{"fieldtype": "Section Break"},
			{"fieldtype": "HTML", "fieldname": "timer_html"}
		]
	});

	if (row) {
		dialog.set_values({
			'activity_type': row.activity,
			'task': row.task+" - "+row.subject,
		});
	}
	dialog.get_field("timer_html").$wrapper.append(get_timer_html());
	function get_timer_html() {
		return `
			<div class="stopwatch" style="text-align: center;font-size: 20px;margin-bottom: 17px;">
				<span class="hours">00</span>
				<span class="colon">:</span>
				<span class="minutes">00</span>
				<span class="colon">:</span>
				<span class="seconds">00</span>
			</div>
			<div class="playpause text-center">
				<button class= "btn btn-primary btn-start"> ${ __("Start") } </button>
				<button class= "btn btn-primary btn-complete"> ${ __("Complete") } </button>
			</div>
		`;
	}
	go1_projects.daily_update.control_timer(frm, dialog, row, timestamp);
	dialog.show();
};

go1_projects.daily_update.control_timer = function(frm, dialog, row, timestamp=0) {
	var $btn_start = dialog.$wrapper.find(".playpause .btn-start");
	var $btn_complete = dialog.$wrapper.find(".playpause .btn-complete");
	var interval = null;
	var currentIncrement = timestamp;
	var initialized = row ? true : false;
	var clicked = false;
	var paused = false	
	var flag = true; // Alert only once
	// If row with not completed status, initialize timer with the time elapsed on click of 'Start Timer'.
	if (row) {
		initialized = true;
		$btn_start.hide();
		$btn_complete.show();
		initializeTimer();
	}

	if (!initialized) {
		$btn_complete.hide();
	}

	$btn_start.click(function(e) {
		if (!initialized) {
			// New activity if no activities found
			let add_child = false
			var args = dialog.get_values();
			if(!args) return;
            const task = args.task
			let split_txt = task.split(" ")[0]
            for(let i of frm.doc.allocate_task){
                if(i.task == split_txt && !i.started && !i.from_time_update && !i.to_time){
					add_child=true
                    i.from_time_update = frappe.datetime.get_datetime_as_string()
                    i.started=1
					i.activity = args.activity
                    frappe.call({
                        method:"go1_projects.api.update_start_timer",
                        args:{
                            "task":split_txt,
                            "time": frappe.datetime.get_datetime_as_string(),
							"activity":args.activity_type
                        }
                    })
                }
            }
			if(!add_child){
				for(let i of frm.doc.allocate_task){
					if(i.task == split_txt){
						frappe.call({
							method:"go1_projects.api.update_task_list",
							async:false,
							args:{
								"t":i,
								"start_time":frappe.datetime.get_datetime_as_string(),
								"activity":args.activity_type
							},callback(r){
								frm.reload_doc()
							}
						})
						break
					}
				}
			}
            frm.refresh_field("allocate_task")
			frm.reload_doc()
		}

		if (clicked) {
			e.preventDefault();
			return false;
		}

		if (!initialized) {
			initialized = true;
			$btn_start.hide();
			$btn_complete.show();
			initializeTimer();
		}
	});

	// Stop the timer and update the time logged by the timer on click of 'Complete' button
	$btn_complete.click(function() {
		var args = dialog.get_values();
		const task = args.task
		let split_txt = task.split(" ")[0]
		const end_time = frappe.datetime.now_datetime();
		const actual_hours = currentIncrement / 3600
		$.each(frm.doc.allocate_task || [], function (i, row) {
			if(row.task == split_txt && row.started && !row.completed){
				row.actual_hours=currentIncrement / 3600;
				row.to_time = end_time;
				row.completed = 1
			}
		});

		frappe.call({
			method:"go1_projects.api.update_end_timer",
			args:{
				"task":split_txt,
				"time": end_time,
				"actual_hours":actual_hours
			}
		})
		frm.refresh_field("allocate_task")
		reset();
		dialog.hide();
		frm.reload_doc()
	});
	function initializeTimer() {
		interval = setInterval(function() {
			var current = setCurrentIncrement();
			updateStopwatch(current);
		}, 1000);
	}

	function updateStopwatch(increment) {
		var hours = Math.floor(increment / 3600);
		var minutes = Math.floor((increment - (hours * 3600)) / 60);
		var seconds = increment - (hours * 3600) - (minutes * 60);

		// If modal is closed by clicking anywhere outside, reset the timer
		if (!$('.modal-dialog').is(':visible')) {
			reset();
		}
		if(hours > 99999)
			reset();
		$(".hours").text(hours < 10 ? ("0" + hours.toString()) : hours.toString());
		$(".minutes").text(minutes < 10 ? ("0" + minutes.toString()) : minutes.toString());
		$(".seconds").text(seconds < 10 ? ("0" + seconds.toString()) : seconds.toString());
	}

	function setCurrentIncrement() {
		currentIncrement += 1;
		return currentIncrement;
	}

	function reset() {
		currentIncrement = 0;
		initialized = false;
		clearInterval(interval);
		$(".hours").text("00");
		$(".minutes").text("00");
		$(".seconds").text("00");
		$btn_complete.hide();
		$btn_start.show();
	}
};