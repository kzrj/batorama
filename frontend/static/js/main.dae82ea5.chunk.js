(this.webpackJsonpdm=this.webpackJsonpdm||[]).push([[0],{15:function(e,t,a){"use strict";a.r(t),a.d(t,"AuthTypes",(function(){return m})),a.d(t,"INITIAL_STATE",(function(){return d})),a.d(t,"AuthSelectors",(function(){return h})),a.d(t,"loginRequest",(function(){return p})),a.d(t,"loginSuccess",(function(){return g})),a.d(t,"loginFailure",(function(){return E})),a.d(t,"signUpRequest",(function(){return b})),a.d(t,"signUpSuccess",(function(){return f})),a.d(t,"signUpFailure",(function(){return v})),a.d(t,"logoutRequest",(function(){return y})),a.d(t,"logoutSuccess",(function(){return O})),a.d(t,"logoutFailure",(function(){return k})),a.d(t,"resetAuthErrors",(function(){return _})),a.d(t,"toggleModal",(function(){return j})),a.d(t,"checkTokenRequest",(function(){return T})),a.d(t,"checkTokenSuccess",(function(){return N})),a.d(t,"checkTokenFail",(function(){return S})),a.d(t,"checkAuthSuccess",(function(){return w})),a.d(t,"reducer",(function(){return C}));var n,r=a(24),l=a(127),c=a(176),o=a.n(c),s=Object(l.createActions)({loginRequest:["data"],loginSuccess:["user"],loginFailure:["error"],signupRequest:["data"],signupSuccess:["user"],signupFailure:["error"],logoutRequest:null,logoutSuccess:null,logoutFailure:["error"],checkTokenRequest:["payload"],checkTokenSuccess:["payload"],checkTokenFail:["error"],resetAuthErrors:null,restorePasswordRequest:["data"],restorePasswordSuccess:null,restorePasswordFailure:["error"],toggleModal:["isAuthModalOpen"],checkAuthRequest:["payload"],checkAuthSuccess:["payload"],checkAuthFail:null}),u=s.Types,i=s.Creators,m=u;t.default=i;var d=o()({fetching:!1,user:null,error:"",isLoggedIn:!1,isLoggingIn:!1}),h={getUser:function(e){return e.user}},p=function(e,t){t.data;return e.merge({fetching:!0,user:null,isLoggingIn:!0,isLoggedIn:!1})},g=function(e,t){var a=t.user;return e.merge({fetching:!1,error:null,user:a,isLoggedIn:!0,isLoggingIn:!1})},E=function(e,t){var a=t.error;return e.merge({fetching:!1,error:a,user:null,isLoggedIn:!1,isLoggingIn:!1})},b=function(e,t){t.data;return e.merge({fetching:!0,user:{},isLoggingIn:!0,isLoggedIn:!1})},f=function(e,t){var a=t.user;return e.merge({fetching:!1,error:null,user:a,isLoggingIn:!1,isLoggedIn:!0})},v=function(e,t){var a=t.error;return e.merge({fetching:!1,error:a,user:null,isLoggingIn:!1,isLoggedIn:!1})},y=function(e){return e.merge({fetching:!0,isLoggingIn:!0})},O=function(e){return e.merge({fetching:!1,error:null,user:null,isLoggingIn:!1,isLoggedIn:!1})},k=function(e,t){var a=t.error;return e.merge({fetching:!1,error:a,isLoggingIn:!1})},_=function(e){return e.merge({fetching:!1,error:null})},j=function(e,t){var a=t.isAuthModalOpen;return e.merge({isAuthModalOpen:a,error:null})},T=function(e,t){t.payload;return e.merge({fetching:!0})},N=function(e,t){var a=t.payload;return e.merge({fetching:!1,error:null,user:a.user,isLoggedIn:!0,isLoggingIn:!1})},S=function(e,t){var a=t.error;return e.merge({fetching:!1,error:a,user:null,isLoggedIn:!1,isLoggingIn:!1})},w=function(e,t){var a=t.payload;return e.merge({user:a,isLoggedIn:!0,isLogginIn:!1})},C=Object(l.createReducer)(d,(n={},Object(r.a)(n,u.LOGIN_REQUEST,p),Object(r.a)(n,u.LOGIN_SUCCESS,g),Object(r.a)(n,u.LOGIN_FAILURE,E),Object(r.a)(n,u.SIGNUP_REQUEST,b),Object(r.a)(n,u.SIGNUP_SUCCESS,f),Object(r.a)(n,u.SIGNUP_FAILURE,v),Object(r.a)(n,u.CHECK_TOKEN_REQUEST,T),Object(r.a)(n,u.CHECK_TOKEN_FAIL,S),Object(r.a)(n,u.CHECK_TOKEN_SUCCESS,N),Object(r.a)(n,u.LOGOUT_REQUEST,y),Object(r.a)(n,u.LOGOUT_SUCCESS,O),Object(r.a)(n,u.LOGOUT_FAILURE,k),Object(r.a)(n,u.TOGGLE_MODAL,j),Object(r.a)(n,u.RESET_AUTH_ERRORS,_),Object(r.a)(n,u.CHECK_AUTH_SUCCESS,w),n))},195:function(e,t,a){e.exports=a(374)},374:function(e,t,a){"use strict";a.r(t);var n=a(24),r=a(0),l=a.n(r),c=a(11),o=a.n(c),s=a(100),u=a(21),i=a(38),m=a(18),d=a(175),h=a(183),p=a(34),g=a.n(p),E=a(20),b=a(27),f=a.n(b),v="".concat("http://35.222.169.29","/api"),y={JWT_AUTH:"".concat(v,"/jwt/api-token-auth/"),JWT_CHECK_TOKEN:"".concat(v,"/jwt/api-token-verify/"),RAMSHIK_SHIFT_CREATE_DATA:"".concat(v,"/ramshik/shifts/create/init_data/"),RAMSHIK_SHIFT_CREATE:"".concat(v,"/ramshik/shifts/create/"),EMPLOYEE_PAYOUT_INIT_DATA:"".concat(v,"/manager/ramshik_payments/init_data/"),EMPLOYEE_PAYOUT:"".concat(v,"/manager/ramshik_payments/ramshik_payout/"),MANAGER_SHIFT_LIST:"".concat(v,"/manager/shift_list/"),KLADMAN_SALE_INIT_DATA:"".concat(v,"/kladman/sales/create/init_data/"),KLADMAN_SALE_CREATE:"".concat(v,"/kladman/sales/create/")},O=function(){return{logIn:function(e){var t=e.username,a=e.password;return f.a.post(y.JWT_AUTH,{username:t,password:a}).then((function(e){if(e.status<200||e.status>=300)throw new Error(e);return{token:e.data.token,user:e.data.user}})).catch((function(e){throw new Error(e.response.data[Object.keys(e.response.data)[0]][0])})).then((function(e){return localStorage.setItem("token",e.token),e.user}))},checkToken:function(e){return f.a.post(y.JWT_CHECK_TOKEN,{token:e}).then((function(e){return{user:e.data.user}})).catch((function(e){throw new Error(e.response.data[Object.keys(e.response.data)[0]][0])}))},logOut:function(){localStorage.removeItem("token")},signUp:function(e){var t=e.email,a=e.phone;return f.a.post(y.SIGNUP,{email:t,phone:a}).then((function(e){return e.data})).catch((function(e){throw new Error(e.response.data[Object.keys(e.response.data)[0]])}))},checkAuth:function(e){var t=localStorage.getItem("token");if(!t)throw new Error("\u041d\u0435\u0442 \u0434\u043e\u0441\u0442\u0443\u043f\u0430");return f.a.post(y.JWT_CHECK_TOKEN,{token:t}).then((function(t){var a=t.data.user,n=a.group;if(-1===e.indexOf(n))throw new Error("\u041d\u0435\u0442 \u0434\u043e\u0441\u0442\u0443\u043f\u0430");return a})).catch((function(e){throw new Error(e.message)}))}}},k=a(15),_=g.a.mark(N),j=g.a.mark(S),T=g.a.mark(w);function N(e,t){var a,n;return g.a.wrap((function(r){for(;;)switch(r.prev=r.next){case 0:return a=t.data,r.next=3,Object(E.c)(k.default.resetAuthErrors());case 3:return r.prev=3,r.next=6,Object(E.b)(e.logIn,a);case 6:return n=r.sent,r.next=9,Object(E.c)(k.default.loginSuccess(n));case 9:return r.next=11,Object(E.c)(k.default.toggleModal(!1));case 11:r.next=17;break;case 13:return r.prev=13,r.t0=r.catch(3),r.next=17,Object(E.c)(k.default.loginFailure(r.t0.message));case 17:case"end":return r.stop()}}),_,null,[[3,13]])}function S(e,t){return g.a.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return t.prev=0,t.next=3,Object(E.b)(e.logOut);case 3:return t.next=5,Object(E.c)(k.default.logoutSuccess());case 5:t.next=11;break;case 7:return t.prev=7,t.t0=t.catch(0),t.next=11,Object(E.c)(k.default.logoutFailure(t.t0.message));case 11:case"end":return t.stop()}}),j,null,[[0,7]])}function w(e,t){var a,n;return g.a.wrap((function(r){for(;;)switch(r.prev=r.next){case 0:return a=t.payload,r.prev=1,r.next=4,Object(E.b)(e.checkToken,a);case 4:return n=r.sent,r.next=7,Object(E.c)(k.default.checkTokenSuccess(n));case 7:r.next=13;break;case 9:return r.prev=9,r.t0=r.catch(1),r.next=13,Object(E.c)(k.default.checkTokenFail(r.t0.message));case 13:case"end":return r.stop()}}),T,null,[[1,9]])}var C=g.a.mark(A),I=O();function A(){return g.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,Object(E.a)([Object(E.d)(k.AuthTypes.LOGIN_REQUEST,N,I),Object(E.d)(k.AuthTypes.LOGOUT_REQUEST,S,I),Object(E.d)(k.AuthTypes.CHECK_TOKEN_REQUEST,w,I)]);case 2:case"end":return e.stop()}}),C)}var x=a(422),L=Object(m.combineReducers)({auth:a(15).reducer,form:x.a}),R=a(182),U=a(30),F=a(31),M=a(25),D=a(33),q=a(32),V=a(417),H=a(83),K=a(420),G=a(419),P=a(416),J=(a(378),a(379),a(381),a(375),a(421),function(e){var t=e.label,a=e.placeholder,n=e.input,r=e.multiline,c=e.meta,o=c.touched,s=c.invalid,u=c.error,i=e.labelClass,m=Object(H.a)(e,["label","placeholder","input","multiline","meta","labelClass"]);return l.a.createElement(P.a,Object.assign({fullWidth:!0,label:t,placeholder:a,error:o&&s,helperText:o&&u},n,m,{multiline:r,InputLabelProps:{className:i}}))});function Q(e){var t=e.parentSubmit,a=e.pristine,n=(e.reset,e.submitting),r=e.handleSubmit;e.eventFetching,e.eventError,e.message;return l.a.createElement("div",{className:"card card-style"},l.a.createElement("div",{className:"content"},l.a.createElement("form",{onSubmit:r(t),className:""},l.a.createElement(K.a,{component:J,label:"\u041b\u043e\u0433\u0438\u043d",name:"username",margin:"dense"}),l.a.createElement(K.a,{component:J,label:"\u041f\u0430\u0440\u043e\u043b\u044c",name:"password",margin:"dense",type:"password"}),l.a.createElement("button",{className:"btn btn-m mt-2 font-900 shadow-s bg-highlight text-wrap",type:"submit",disabled:a||n},"\u0412\u043e\u0439\u0442\u0438"))))}function W(e){var t=Object(u.g)();return l.a.createElement("div",{className:"card-style mx-0 my-1 pt-2",onClick:function(){t.push(e.to)},style:{background:"white",color:"white","font-weight":"bold","font-size":"1.5em","text-align":"center","word-break":"break-word","border-radius":"15px","line-height":"12px"}},l.a.createElement("p",null,e.title))}function Y(e){var t=e.user;e.logout;return t.is_senior_ramshik&&u.a,t.is_manager,t.is_kladman&&l.a.createElement("div",{className:" "},l.a.createElement(W,{title:"\u0421\u043a\u043b\u0430\u0434. \u0422\u0435\u043a\u0443\u0448\u0438\u0435 \u043e\u0441\u0442\u0430\u0442\u043a\u0438",to:"/manager/ramshik_payments/"}),l.a.createElement(W,{title:"\u0421\u043e\u0437\u0434\u0430\u0442\u044c \u043f\u0440\u043e\u0434\u0430\u0436\u0443",to:"/kladman/sales/create_sale/"}),l.a.createElement(W,{title:"\u041f\u0440\u043e\u0434\u0430\u0436\u0438 \u0441\u043f\u0438\u0441\u043e\u043a",to:"/kladman/create_sales/"}))}Q=Object(G.a)({form:"loginForm",validate:function(e){var t={};return["username","password"].forEach((function(a){e[a]||(t[a]="\u041e\u0431\u044f\u0437\u0430\u0442\u0435\u043b\u044c\u043d\u043e\u0435 \u043f\u043e\u043b\u0435")})),t}})(Q);var z=function(e){Object(D.a)(a,e);var t=Object(q.a)(a);function a(e){var n;return Object(U.a)(this,a),(n=t.call(this,e)).state={username:"",password:""},n.login=n.login.bind(Object(M.a)(n)),n}return Object(F.a)(a,[{key:"componentDidMount",value:function(){}},{key:"login",value:function(){this.props.login(this.props.form.values)}},{key:"render",value:function(){var e=this.props.state.auth,t=e.isLoggedIn,a=e.fetching,n=e.user;return a?l.a.createElement(V.a,null):t?l.a.createElement(Y,{user:n,logout:this.props.logout}):l.a.createElement(Q,{parentSubmit:this.login})}}]),a}(r.Component),B=Object(i.b)((function(e){return{routing:e.routing,state:e,form:e.form.loginForm}}),(function(e){return{login:function(t){return e(k.default.loginRequest(t))},logout:function(t){return e(k.default.logoutRequest(t))},checkToken:function(t){return e(k.default.checkTokenRequest(t))}}}))(z);function X(e){var t=Object(u.g)();return l.a.createElement("div",{className:"d-flex justify-content-between align-items-baseline px-3 py-2"},l.a.createElement("h4",{onClick:function(){t.push("/")}},"\u0420\u0430\u043c\u0430"),l.a.createElement("button",{className:"btn btn-sx bg-red1-light",onClick:function(){e.logout(),t.push("/")}},"\u0432\u044b\u0439\u0442\u0438"))}var Z=function(e){Object(D.a)(a,e);var t=Object(q.a)(a);function a(e){var n;return Object(U.a)(this,a),(n=t.call(this,e)).state={modalOpen:!1},n}return Object(F.a)(a,[{key:"componentDidMount",value:function(){var e=localStorage.getItem("token");e&&this.props.checkToken(e)}},{key:"render",value:function(){var e=this.props.auth;e.isLoggedIn,e.fetching;return e.user?l.a.createElement("div",{className:"header"},l.a.createElement(X,{logout:this.props.logout})):""}}]),a}(r.Component),$=Object(i.b)((function(e){return{state:e,auth:e.auth,routing:e.routing}}),(function(e){return{checkToken:function(t){return e(k.default.checkTokenRequest(t))},logout:function(){return e(k.default.logoutRequest())}}}))(Z),ee=a(16);function te(e){var t=e.lastOperations;return l.a.createElement("div",{className:"card card-style mt-0"},l.a.createElement("div",{className:"content"},l.a.createElement("h4",null,"\u041f\u043e\u0441\u043b\u0435\u0434\u043d\u0438\u0435 10 \u043e\u043f\u0435\u0440\u0430\u0446\u0438\u0438"),t.length>0?l.a.createElement("table",{className:"table table-sm table-responsive",style:{lineHeight:"16px"}},l.a.createElement("thead",{className:""},l.a.createElement("th",null,"\u0414\u0430\u0442\u0430"),l.a.createElement("th",null,"\u0422\u0438\u043f"),l.a.createElement("th",null,"\u0421\u043e\u0442\u0440\u0443\u0434\u043d\u0438\u043a"),l.a.createElement("th",null,"\u0421\u0443\u043c\u043c\u0430")),l.a.createElement("tbody",null,t.map((function(e){return l.a.createElement("tr",null,l.a.createElement("td",{className:"text-nowrap"},e.created_at),l.a.createElement("td",null,"withdraw_employee"===e.record_type?"\u041e\u0431\u043d\u0430\u043b \u0440\u0430\u043c\u0449\u0438\u043a\u0443":"\u0417\u0430\u0447\u0438\u0441\u043b\u0435\u043d\u0438\u0435 \u0440\u0430\u043c\u0449\u0438\u043a\u0443 \u0441\u043e \u0441\u043c\u0435\u043d\u044b"),l.a.createElement("td",null,e.employee),l.a.createElement("td",{className:"withdraw_employee"===e.record_type?"color-red1-light font-16":"color-green1-light font-16"},"withdraw_employee"===e.record_type?"-"+e.amount:"+"+e.amount))})))):l.a.createElement("div",null,"\u041d\u0435\u0442 \u043e\u043f\u0435\u0440\u0430\u0446\u0438\u0438")))}var ae=function(e){Object(D.a)(a,e);var t=Object(q.a)(a);function a(e){var n;return Object(U.a)(this,a),(n=t.call(this,e)).state={employees:[],activeEmployee:null,amount:0,last_payouts:[],message:null,error:null},n.payout=n.payout.bind(Object(M.a)(n)),n}return Object(F.a)(a,[{key:"componentDidMount",value:function(){var e=this;f.a.get(y.EMPLOYEE_PAYOUT_INIT_DATA).then((function(t){var a=t.data;e.setState(Object(ee.a)(Object(ee.a)({},e.state),{},{employees:a.employees,last_payouts:a.last_payouts}))}))}},{key:"payout",value:function(){var e=this,t=this.state,a=t.activeEmployee,n=t.amount,r=localStorage.getItem("token"),l=new FormData;l.append("employee",a.id),l.append("amount",n),f()({method:"post",url:y.EMPLOYEE_PAYOUT,data:l,headers:{"content-type":"multipart/form-data",Authorization:"JWT ".concat(r)}}).then((function(t){e.setState(Object(ee.a)(Object(ee.a)({},e.state),{},{message:t.data.message,employees:t.data.employees,activeEmployee:null,last_payouts:t.data.last_payouts}))})).catch((function(t){var a=new Error(t);throw a.data=function(e){if(e&&"undefined"!==typeof e.response){var t={status:e.response.status,statusText:e.response.statusText,message:null,response:e.response};if("message"in e.response.data)t.message=JSON.stringify(e.response.data.message);else{var a="";for(var n in e.response.data)a+="".concat(n,": ").concat(e.response.data[n],". ");t.message=a}return t}return{status:"Connection Error",statusText:"An error occurred while sending your data!",message:"An error occurred while sending your data!"}}(t),e.setState({message:"\u041e\u0448\u0438\u0431\u043a\u0430"}),a}))}},{key:"render",value:function(){var e=this,t=this.state,a=t.employees,n=t.activeEmployee,r=t.amount,c=t.message,o=t.last_payouts;return l.a.createElement("div",{className:"mt-2"},l.a.createElement("div",{className:"card card-style mb-2"},l.a.createElement("div",{className:"content"},l.a.createElement("h4",{className:"mb-2"},"\u0420\u0430\u0441\u0447\u0435\u0442 \u0440\u0430\u043c\u0449\u0438\u043a\u043e\u0432"),l.a.createElement("div",{className:"d-flex justify-content-start"},a.length>0&&l.a.createElement("table",{className:"table table-sm table-responsive w-75 mr-2"},l.a.createElement("thead",null,l.a.createElement("th",null,"\u0440\u0430\u043c\u0449\u0438\u043a"),l.a.createElement("th",null,"\u0431\u0430\u043b\u0430\u043d\u0441")),l.a.createElement("tbody",null,a.map((function(t){return l.a.createElement("tr",{className:n&&n.id===t.id&&"bg-green1-light",onClick:function(){return e.setState(Object(ee.a)(Object(ee.a)({},e.state),{},{activeEmployee:t,message:null}))}},l.a.createElement("td",null,t.nickname),l.a.createElement("td",null,t.cash," \u0440"))})))),n&&l.a.createElement("div",null,l.a.createElement("span",{className:"font-16 mr-3"},n.nickname),l.a.createElement("span",{className:"font-16 font-600"},n.cash," \u0440"),l.a.createElement(P.a,{type:"number",className:"my-1",value:r,onChange:function(t){return e.setState(Object(ee.a)(Object(ee.a)({},e.state),{},{amount:t.target.value}))}}),l.a.createElement("button",{className:"d-block btn btn-m bg-green2-light mt-2",onClick:this.payout},"\u0412\u044b\u0434\u0430\u0442\u044c")),c&&l.a.createElement("p",{className:"color-dark text-center"},c)))),l.a.createElement(te,{lastOperations:o}))}}]),a}(r.Component);function ne(e){return l.a.createElement("table",{className:"table table-sm table-responsive"},l.a.createElement("thead",null,l.a.createElement("th",null,"\u0414\u0430\u0442\u0430 \u0434\u0435\u043d\u044c/\u043d\u043e\u0447\u044c"),l.a.createElement("th",null,"\u041f\u0438\u043b\u043e\u043c\u0430\u0442"),l.a.createElement("th",null,"\u041e\u0431\u0449\u0438\u0439 \u043e\u0431\u044c\u0435\u043c"),l.a.createElement("th",null,"\u0420\u0430\u043c\u0449\u0438\u043a\u0438"),l.a.createElement("th",null,"\u0437\u0430 \u0440\u0430\u0431\u043e\u0442\u0443 \u043e\u0431\u0449/\u043d\u0430 \u0447\u0435\u043b\u0430")),l.a.createElement("tbody",null,e.shiftList.map((function(e){return l.a.createElement("tr",null,l.a.createElement("td",null,e.date),l.a.createElement("td",null,e.lumber_records.map((function(e){return l.a.createElement("span",{className:"d-block mb-2",style:{lineHeight:"16px"}},l.a.createElement("span",{className:"mr-1 d-block"},e.lumber),l.a.createElement("span",{className:"mr-1"},e.quantity,"\u0448\u0442"),l.a.createElement("span",{className:"mr-1"},e.volume,"\u043c3"),l.a.createElement("span",{className:""},e.rate,"\u0440"))}))),l.a.createElement("td",null,e.volume,"\u043c3"),l.a.createElement("td",null,l.a.createElement("span",{className:"d-block"},e.initiator),e.employees.map((function(e){return l.a.createElement("span",{className:"d-block"},e)}))),l.a.createElement("td",null,l.a.createElement("span",{className:"d-block"},e.employee_cash,"\u0440 "),l.a.createElement("span",null," ",e.cash_per_employee,"\u0440")))}))))}var re=function(e){Object(D.a)(a,e);var t=Object(q.a)(a);function a(e){var n;return Object(U.a)(this,a),(n=t.call(this,e)).state={shiftList:[],message:null,error:null},n}return Object(F.a)(a,[{key:"componentDidMount",value:function(){var e=this,t=localStorage.getItem("token");f()({method:"get",url:y.MANAGER_SHIFT_LIST,headers:{Authorization:"JWT ".concat(t)}}).then((function(t){e.setState(Object(ee.a)(Object(ee.a)({},e.state),{},{shiftList:t.data.results}))}))}},{key:"render",value:function(){var e=this.state.shiftList;return l.a.createElement("div",{className:"mt-2"},l.a.createElement("div",{className:"card card-style mb-2"},l.a.createElement("div",{className:"content"},l.a.createElement("h4",{className:"mb-2"},"\u0421\u043c\u0435\u043d\u044b"),e.length>0?l.a.createElement(ne,{shiftList:e}):l.a.createElement("h5",null,"\u041d\u0435\u0442 \u0441\u043c\u0435\u043d"))))}}]),a}(r.Component),le=a(55),ce=a(132),oe=a.n(ce);function se(e,t){var a=function(e,t){var a=null;return e.map((function(e){e.id==t&&(a=e)})),a}(e,t.id),n=e.indexOf(a);return e=[].concat(Object(le.a)(e.slice(0,n)),[t],Object(le.a)(e.slice(n+1)))}function ue(e){var t=e.totalCash,a=e.employees,n=e.activeEmployees,r=e.addEmployee;return l.a.createElement("div",{className:"content"},l.a.createElement("h4",null,"\u041a\u0442\u043e \u0440\u0430\u0431\u043e\u0442\u0430\u043b? ",n.length>0&&"("+n.length+")"),l.a.createElement("div",{className:"d-flex justify-content-between my-2"},a.map((function(e){return l.a.createElement("div",{className:n.includes(e)?"bg-green2-light rounded-xs px-2 py-2 ":"bg-dark1-dark rounded-xs px-2 py-2 ",onClick:function(){return r(e)}},e.nickname)}))),n.length>0&&l.a.createElement("div",null,l.a.createElement("div",{className:"d-flex justify-content-start"},n.map((function(e){return l.a.createElement("div",{className:"mx-2"},l.a.createElement("span",{className:"d-block font-16"},e.nickname),t>0&&l.a.createElement("span",{className:"font-17 font-600"}," ",(t/n.length).toFixed(0)," \u0440\u0443\u0431"))})))))}var ie=function(e){Object(D.a)(a,e);var t=Object(q.a)(a);function a(e){var n;return Object(U.a)(this,a),(n=t.call(this,e)).state={lumbers:[],initLumbers:[],totalVolume:0,totaCash:0,employees:[],activeEmployees:[],message:null,error:null},n.calcRow=n.calcRow.bind(Object(M.a)(n)),n.calcRowAndTotal=n.calcRowAndTotal.bind(Object(M.a)(n)),n.calcTotalVolume=n.calcTotalVolume.bind(Object(M.a)(n)),n.calcTotalCash=n.calcTotalCash.bind(Object(M.a)(n)),n.addEmployee=n.addEmployee.bind(Object(M.a)(n)),n.saveData=n.saveData.bind(Object(M.a)(n)),n}return Object(F.a)(a,[{key:"componentDidMount",value:function(){var e=this;f.a.get(y.RAMSHIK_SHIFT_CREATE_DATA).then((function(t){var a=t.data;e.setState({lumbers:a.lumbers,initLumbers:a.lumbers,employees:a.employees})}))}},{key:"calcRow",value:function(e,t,a){var n=e.employee_rate;return a&&600==e.employee_rate&&(n=650),a||650!=e.employee_rate||(n=600),a||600!=e.employee_rate||(n=e.employee_rate),Object(ee.a)(Object(ee.a)({},e),{},{lumber:e.id,quantity:t,volume_total:t*e.volume,cash:t*e.volume*n,employee_rate:n})}},{key:"calcTotalVolume",value:function(e){var t=0;return e.map((function(e){t+=e.volume_total})),t}},{key:"calcTotalCash",value:function(e){var t=0;return e.map((function(e){t+=e.cash})),t}},{key:"calcRowAndTotal",value:function(e,t){var a=this,n=this.state.lumbers,r=this.calcRow(t,e.target.value,!1);n=se(n,r);var l=this.calcTotalVolume(n);l>=10?(n.map((function(e,t){n[t]=a.calcRow(e,e.quantity,!0)})),l=this.calcTotalVolume(n)):(n.map((function(e,t){n[t]=a.calcRow(e,e.quantity,!1)})),l=this.calcTotalVolume(n));var c=this.calcTotalCash(n);this.setState(Object(ee.a)(Object(ee.a)({},this.state),{},{lumbers:n,totalVolume:l,totalCash:c,message:null}))}},{key:"addEmployee",value:function(e){var t=this.state.activeEmployees;t=function(e,t){for(var a=!1,n=-1,r=0;r<e.length;r++)if(e[r].id===t.id){a=!0,n=r;break}return a?(e.splice(n,1),e):[].concat(Object(le.a)(e),[t])}(t,e),this.setState(Object(ee.a)(Object(ee.a)({},this.state),{},{activeEmployees:t}))}},{key:"saveData",value:function(){var e=this,t=this.state,a=t.lumbers,n=t.totalCash,r=t.totalVolume,l=t.activeEmployees,c=localStorage.getItem("token"),o=[];l.map((function(e){return t=o,a=e.id,o=oe.a.xor(t,[a]);var t,a}));var s={shift_type:"day",date:null,raw_records:a,employees:o,employee_cash:n,volume:r};f()({method:"post",url:y.RAMSHIK_SHIFT_CREATE,data:s,headers:{"content-type":"application/JSON",Authorization:"JWT ".concat(c)}}).then((function(t){e.setState({message:"\u0414\u0430\u043d\u043d\u044b\u0435 \u0437\u0430\u043f\u0438\u0441\u0430\u043d\u044b."})})).catch((function(t){e.setState({message:"\u041e\u0448\u0438\u0431\u043a\u0430"})})),this.setState({activeEmployees:[],lumbers:this.state.initLumbers,totalVolume:0,totalCash:0})}},{key:"render",value:function(){var e=this,t=this.state,a=t.lumbers,n=t.totalVolume,r=t.totalCash,c=t.employees,o=t.activeEmployees,s=t.message;return l.a.createElement("div",null,l.a.createElement("div",{className:"card card-style mb-1 mt-2"},l.a.createElement("div",{className:"content"},l.a.createElement("h2",null,"\u0421\u043c\u0435\u043d\u0430"),a.length>0&&l.a.createElement("table",{className:"table table-sm table-responsive text-center",style:{lineHeight:"17px",color:"#6c6c6c"}},l.a.createElement("thead",null,l.a.createElement("th",null,"\u0418\u0437\u0434\u0435\u043b\u0438\u0435"),l.a.createElement("th",null,"\u041a\u043e\u043b-\u0432\u043e"),l.a.createElement("th",null,"\u041e\u0431\u044c\u0435\u043c"),l.a.createElement("th",null,"\u0421\u0442\u0430\u0432\u043a\u0430"),l.a.createElement("th",null,"\u0421\u0443\u043c\u043c\u0430")),l.a.createElement("tbody",null,a.map((function(t,a){return l.a.createElement("tr",{key:a},l.a.createElement("td",null,t.name),l.a.createElement("td",{className:"w-25"},l.a.createElement("input",{style:{color:"#6c6c6c"},type:"number",className:"w-75",onChange:function(a){return e.calcRowAndTotal(a,t)},value:t.quantity>0&&t.quantity})),l.a.createElement("td",null,t.volume_total>0&&t.volume_total.toFixed(3)+" \u043c3"),l.a.createElement("td",null,t.employee_rate," \u0440\u0443\u0431"),l.a.createElement("td",null,t.cash>0&&t.cash.toFixed(0)+" \u0440\u0443\u0431"))})),l.a.createElement("tr",null,l.a.createElement("td",null,"\u0418\u0442\u043e\u0433\u043e"),l.a.createElement("td",{className:"w-25"},"-"),l.a.createElement("td",null,l.a.createElement("span",{className:"font-17 font-600"},n>0&&n.toFixed(4)+" \u043c3")),l.a.createElement("td",null,"-"),l.a.createElement("td",null,l.a.createElement("span",{className:"font-17 font-600"},r>0&&r.toFixed(0)+" \u0440\u0443\u0431"))))))),l.a.createElement("div",{className:"card card-style mb-3"},l.a.createElement(ue,{totalCash:r,employees:c,activeEmployees:o,addEmployee:this.addEmployee})),o.length>0&&r>0&&l.a.createElement("button",{onClick:this.saveData,className:"btn btn-center-xl btn-xxl text-uppercase font-900 bg-highlight rounded-sm shadow-l"},"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u0434\u0430\u043d\u043d\u044b\u0435"),s&&l.a.createElement("h2",{className:"color-green1-light text-center"},"\u0414\u0430\u043d\u043d\u044b\u0435 \u0441\u043e\u0445\u0440\u0430\u043d\u0435\u043d\u044b!"))}}]),a}(r.Component);var me=function(e){Object(D.a)(a,e);var t=Object(q.a)(a);function a(e){var n;return Object(U.a)(this,a),(n=t.call(this,e)).state={lumbers:[],initLumbers:[],totalVolume:0,totaCash:0,employees:[],activeEmployees:[],message:null,error:null},n.calcRowQnty=n.calcRowQnty.bind(Object(M.a)(n)),n.calcRowVolume=n.calcRowVolume.bind(Object(M.a)(n)),n.calcRowCash=n.calcRowCash.bind(Object(M.a)(n)),n.calcTotal=n.calcTotal.bind(Object(M.a)(n)),n.saveData=n.saveData.bind(Object(M.a)(n)),n}return Object(F.a)(a,[{key:"componentDidMount",value:function(){var e=this;f.a.get(y.KLADMAN_SALE_INIT_DATA).then((function(t){var a=t.data;e.setState({lumbers:a.lumbers,initLumbers:a.lumbers})}))}},{key:"calcRowQnty",value:function(e,t){var a=this.state.lumbers;t.quantity=e.target.value,t.volume_total=t.quantity*t.volume,t.cash=t.volume_total*t.rate,a=se(a,t);var n=this.calcTotal(a),r=n.totalCash,l=n.totalVolume;this.setState(Object(ee.a)(Object(ee.a)({},this.state),{},{lumbers:a,totalCash:r,totalVolume:l}))}},{key:"calcRowVolume",value:function(e,t){var a=this.state.lumbers;t.volume_total=e.target.value,t.quantity=t.volume_total/t.volume,t.cash=t.volume_total*t.rate,a=se(a,t);var n=this.calcTotal(a),r=n.totalCash,l=n.totalVolume;this.setState(Object(ee.a)(Object(ee.a)({},this.state),{},{lumbers:a,totalCash:r,totalVolume:l}))}},{key:"calcRowCash",value:function(e,t){var a=this.state.lumbers;t.rate=e.target.value,t.cash=t.volume_total*t.rate,a=se(a,t);var n=this.calcTotal(a),r=n.totalCash,l=n.totalVolume;this.setState(Object(ee.a)(Object(ee.a)({},this.state),{},{lumbers:a,totalCash:r,totalVolume:l}))}},{key:"calcTotal",value:function(e){var t=0,a=0;return e.map((function(e){t+=e.cash,a+=parseFloat(e.volume_total)})),{totalCash:t,totalVolume:a}}},{key:"saveData",value:function(){var e=this,t=this.state,a=t.lumbers,n=t.totalCash,r=t.totalVolume,l=localStorage.getItem("token"),c={raw_records:a,date:null,totalCash:n,totalVolume:r};f()({method:"post",url:y.KLADMAN_SALE_CREATE,data:c,headers:{"content-type":"application/JSON",Authorization:"JWT ".concat(l)}}).then((function(t){e.setState({message:"\u0414\u0430\u043d\u043d\u044b\u0435 \u0437\u0430\u043f\u0438\u0441\u0430\u043d\u044b."})})).catch((function(t){e.setState({message:"\u041e\u0448\u0438\u0431\u043a\u0430"})})),this.setState({lumbers:this.state.initLumbers,totalVolume:0,totalCash:0})}},{key:"render",value:function(){var e=this,t=this.state,a=t.lumbers,n=t.totalVolume,r=t.totalCash,c=t.message;return l.a.createElement("div",null,l.a.createElement("div",{className:"card card-style mb-1 mt-2"},l.a.createElement("div",{className:"content"},l.a.createElement("h2",null,"\u0427\u0442\u043e \u043f\u0440\u043e\u0434\u0430\u0435\u043c?"),a.length>0&&l.a.createElement("table",{className:"table table-sm table-responsive text-center",style:{lineHeight:"17px",color:"#6c6c6c"}},l.a.createElement("thead",null,l.a.createElement("th",null,"\u0418\u0437\u0434\u0435\u043b\u0438\u0435"),l.a.createElement("th",null,"\u041a\u043e\u043b-\u0432\u043e"),l.a.createElement("th",null,"\u041e\u0431\u044c\u0435\u043c"),l.a.createElement("th",null,"\u0421\u0442\u0430\u0432\u043a\u0430"),l.a.createElement("th",null,"\u0421\u0443\u043c\u043c\u0430")),l.a.createElement("tbody",null,a.map((function(t,a){return l.a.createElement("tr",{key:a},l.a.createElement("td",null,t.name),l.a.createElement("td",{className:"w-25"},l.a.createElement("input",{style:{color:"#6c6c6c",width:"50px"},type:"number",onChange:function(a){return e.calcRowQnty(a,t)},value:t.quantity>0&&t.quantity})," \u0448\u0442"),l.a.createElement("td",null,l.a.createElement("input",{style:{color:"#6c6c6c",width:"50px"},type:"number",onChange:function(a){return e.calcRowVolume(a,t)},value:t.volume_total>0&&t.volume_total})," \u043c3"),l.a.createElement("td",null,l.a.createElement("input",{style:{color:"#6c6c6c",width:"50px"},type:"number",onChange:function(a){return e.calcRowCash(a,t)},value:t.rate>0&&t.rate})," \u0440\u0443\u0431"),l.a.createElement("td",null,t.cash>0&&t.cash.toFixed(0)+" \u0440"))})),l.a.createElement("tr",null,l.a.createElement("td",null,"\u0418\u0442\u043e\u0433\u043e"),l.a.createElement("td",{className:"w-25"},"-"),l.a.createElement("td",null,l.a.createElement("span",{className:"font-17 font-600"},n)),l.a.createElement("td",null,"-"),l.a.createElement("td",null,l.a.createElement("span",{className:"font-17 font-600"},r>0&&r.toFixed(0)+" \u0440\u0443\u0431"))))))),r>0&&l.a.createElement("button",{onClick:this.saveData,className:"btn btn-center-xl btn-xxl text-uppercase font-900 bg-highlight rounded-sm shadow-l"},"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u0434\u0430\u043d\u043d\u044b\u0435"),c&&l.a.createElement("h2",{className:"color-green1-light text-center"},"\u0414\u0430\u043d\u043d\u044b\u0435 \u0441\u043e\u0445\u0440\u0430\u043d\u0435\u043d\u044b!"))}}]),a}(r.Component);function de(e,t){var a=function(a){Object(D.a)(r,a);var n=Object(q.a)(r);function r(){return Object(U.a)(this,r),n.apply(this,arguments)}return Object(F.a)(r,[{key:"componentDidMount",value:function(){var e=localStorage.getItem("token");e&&this.props.checkToken(e)}},{key:"render",value:function(){var a=this.props.state.auth,n=a.fetching,r=a.user;return!0!==this.props.isLoggedIn||t||!0,this.props.isLoggedIn&&"manager"===t&&r.is_manager&&!0,this.props.isLoggedIn&&"senior_ramshik"===t&&r.is_senior_ramshik&&!0,this.props.isLoggedIn&&"kladman"===t&&r.is_kladman&&!0,n?l.a.createElement("p",null,"Loading"):this.props.isLoggedIn?l.a.createElement(e,this.props):null}}]),r}(l.a.Component);return Object(i.b)((function(e){return{isLoggedIn:e.auth.isLoggedIn,user:e.auth.user,state:e}}),(function(e){return{checkToken:function(t){return e(k.default.checkTokenRequest(t))}}}))(a)}var he=function(e){var t=Object(h.a)(),a=Object(m.createStore)(L,Object(d.composeWithDevTools)(Object(m.applyMiddleware)(t)));t.run(A);return a}();o.a.render(l.a.createElement(i.a,{store:he},l.a.createElement(R.a,{maxSnack:3},l.a.createElement(s.a,null,l.a.createElement("div",Object(n.a)({className:"app",id:"page"},"className",""),l.a.createElement($,null),l.a.createElement("div",{className:"page-content header-clear"},l.a.createElement(u.d,null,l.a.createElement(u.b,{exact:!0,path:"/",component:B}),l.a.createElement(u.b,{exact:!0,path:"/manager/ramshik_payments/",component:de(ae,"manager")}),l.a.createElement(u.b,{exact:!0,path:"/manager/shift_list/",component:de(re,"manager")}),l.a.createElement(u.b,{exact:!0,path:"/shift/create_shift/",component:de(ie,"is_senior_ramshik")}),l.a.createElement(u.b,{exact:!0,path:"/kladman/sales/create_sale/",component:de(me,"kladman")}))))))),document.getElementById("root"))}},[[195,1,2]]]);
//# sourceMappingURL=main.dae82ea5.chunk.js.map