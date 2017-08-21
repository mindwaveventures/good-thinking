module State exposing (init, update, subscriptions)

import Types exposing (..)
import Rest exposing (..)
import Ports exposing (..)


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
                []
                False
                flags.order
            )
    in
        update (GetData (create_query model)) model


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        NoOp ->
            ( model, Cmd.none )

        ChangePosition newPosition ->
            if not (xor (newPosition < 1) (newPosition > 3)) then
                ( { model | position = newPosition }, Cmd.none )
            else
                ( model, Cmd.none )

        UpdateTags tags ->
            ( model, getData (create_query model) )

        SelectTag tag ->
            let
                new_model =
                    { model | selected_tags = update_selected model tag }
            in
                ( new_model, selectTag new_model.selected_tags )

        QueryComplete response ->
            case response of
                Ok result ->
                    ( { model | resources = result }, listeners () )

                Err error ->
                    ( model, Cmd.none )

        GetData url ->
            ( model, getData url )

        ToggleOrderBox ->
            ( { model | order_box_visible = not model.order_box_visible }, Cmd.none )

        UpdateOrder order ->
            if not (order == model.order_by) then
                let
                    new_model =
                        { model | order_by = order }
                in
                    ( new_model, getData (create_query new_model) )
            else
                ( model, Cmd.none )

        CloseAndUpdate order ->
            update (UpdateOrder order) { model | order_box_visible = False }


update_selected : Model -> Tag -> List Tag
update_selected model tag =
    if List.member tag model.selected_tags then
        List.filter (\t -> t /= tag) model.selected_tags
    else
        tag :: model.selected_tags


create_query : Model -> String
create_query model =
    List.foldl (\a b -> b ++ a.tag_type ++ "=" ++ a.name ++ "&") "?" model.selected_tags ++ "&order=" ++ model.order_by


subscriptions : Model -> Sub Msg
subscriptions model =
    updateTags UpdateTags
