module State exposing (init, update, subscriptions)

import Types exposing (..)
import Rest exposing (..)
import Ports exposing (..)
import Task
import Time
import Process


init : Flags -> ( Model, Cmd Msg )
init flags =
    let
        model =
            (Model
                flags.issue_tags
                flags.reason_tags
                flags.content_tags
                flags.issue_label
                flags.content_label
                flags.reason_label
                flags.selected_tags
                1
                1
                []
                []
                False
                flags.order
                flags.search
                False
                flags.page
                0
                0
                flags.tagHeight
            )
    in
        update (GetInitialData (create_query model)) model


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        NoOp ->
            ( model, Cmd.none )

        ChangePosition newPosition ->
            if not (xor (newPosition < 1) (newPosition > 3)) then
                ( { model | tag_position = newPosition, results_updated = 0 }, Cmd.none )
            else
                ( model, Cmd.none )

        ChangeTipPosition newPosition ->
            if not (xor (newPosition < 1) (newPosition > 3)) then
                ( { model | tip_position = newPosition }, Cmd.none )
            else
                ( model, Cmd.none )

        UpdateTags tags ->
            ( model, getData (create_query model) QueryComplete )

        SelectTag tag ->
            let
                new_model =
                    { model | selected_tags = update_selected model tag }
            in
                ( new_model, selectTag tag )

        QueryComplete response ->
            case response of
                Ok result ->
                    ( { model
                        | resources = result.resources
                        , resource_count = result.count
                        , tips = result.tips
                      }
                    , listeners ()
                    )

                Err error ->
                    ( model, Cmd.none )

        ToggleOrderBox ->
            ( { model | order_box_visible = not model.order_box_visible }, Cmd.none )

        UpdateOrder order ->
            if not (order == model.order_by) then
                let
                    new_model =
                        { model | order_by = order }
                in
                    ( new_model, save_order new_model )
            else
                ( model, Cmd.none )

        CloseAndUpdate order ->
            update (UpdateOrder order) { model | order_box_visible = False }

        Swipe dir ->
            case dir of
                "right" ->
                    update (ChangePosition (model.tag_position - 1)) model

                "left" ->
                    update (ChangePosition (model.tag_position + 1)) model

                _ ->
                    update NoOp model

        TipSwipe dir ->
            case dir of
                "right" ->
                    update (ChangeTipPosition (model.tip_position - 1)) model

                "left" ->
                    update (ChangeTipPosition (model.tip_position + 1)) model

                _ ->
                    update NoOp model

        ShowMore show ->
            ( { model | show_more = show }, Cmd.none )

        GetInitialData url ->
            ( model, getData (url ++ "&page=initial") (LazyLoad url) )

        LazyLoad url response ->
            case response of
                Ok result ->
                    ( { model
                        | resources = result.resources
                        , resource_count = result.count
                        , tips = result.tips
                      }
                    , getData (url ++ "&page=remainder") (LazyRemainder url)
                    )

                Err error ->
                    ( model, Cmd.none )

        LazyRemainder url response ->
            case response of
                Ok result ->
                    ( { model
                        | resources = List.append model.resources result.resources
                      }
                    , listeners ()
                    )

                Err error ->
                    ( model, Cmd.none )

        ResultsLoadingAlert old_pos new_pos ->
            ( { model | results_updated = old_pos }, results_loading new_pos )


update_selected : Model -> Tag -> List Tag
update_selected model tag =
    if List.member tag model.selected_tags then
        List.filter (\t -> t /= tag) model.selected_tags
    else
        tag :: model.selected_tags


create_query : Model -> String
create_query model =
    List.foldl (\a b -> b ++ a.tag_type ++ "=" ++ a.name ++ "&") "?" model.selected_tags
        ++ ("&order=" ++ model.order_by ++ "&q=" ++ model.search ++ "&slug=" ++ model.page)


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.batch
        [ updateTags UpdateTags
        , swipe Swipe
        , tipSwipe TipSwipe
        ]


save_order new_model =
    Task.andThen
        |> (\_ -> getData (create_query new_model) QueryComplete)
        |> (\_ -> changeOrder new_model.order_by)


delay : Time.Time -> msg -> Cmd msg
delay time msg =
    Process.sleep time
        |> Task.perform (\_ -> msg)


results_loading : Int -> Cmd Msg
results_loading new_pos =
    delay (Time.second * 0.5) (ChangePosition new_pos)
